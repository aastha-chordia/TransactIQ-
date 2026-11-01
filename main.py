import json, uuid
from pathlib import Path
import fitz
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import Base, engine, get_db
from .models import Payment, AuditEvent
from .schemas import PaymentCreate, PaymentOut
from .services import predict_risk, choose_route, policy_flags, train_if_missing

Base.metadata.create_all(bind=engine)
train_if_missing()
app = FastAPI(title="TransactIQ API", version="1.0.0",
              description="Educational cross-border payment intelligence simulator.")
STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")

def add_audit(db, ref, action, details=""):
    db.add(AuditEvent(payment_reference=ref, action=action, details=details))
    db.commit()

def as_eur(amount, currency):
    # Demonstration-only approximate conversion table; not live FX.
    rates = {"EUR":1.0, "USD":0.92, "GBP":1.17, "INR":0.011, "AED":0.25, "CAD":0.68}
    return amount * rates.get(currency.upper(), 1.0)

@app.get("/", response_class=HTMLResponse)
def home():
    return (STATIC / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status":"ok", "service":"TransactIQ", "mode":"simulation"}

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return {
        "total_payments": len(payments),
        "total_value": round(sum(p.amount for p in payments), 2),
        "high_risk": sum(p.risk_level in ("High","Critical") for p in payments),
        "pending_approval": sum(p.status == "Pending Approval" for p in payments),
        "settled": sum(p.status == "Settled" for p in payments),
        "failed": sum(p.status == "Failed" for p in payments),
        "payments": [PaymentOut.model_validate(p).model_dump() for p in sorted(payments, key=lambda x:x.id, reverse=True)[:12]]
    }

@app.get("/api/payments", response_model=list[PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).order_by(desc(Payment.id)).all()

@app.post("/api/payments", response_model=PaymentOut)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["country"] = data["country"].upper()
    data["currency"] = data["currency"].upper()
    data["amount_eur"] = as_eur(data["amount"], data["currency"])
    score, level, explanation = predict_risk(data)
    data["risk_score"], data["risk_level"] = score, level
    flags = policy_flags(data)
    data["policy_flags"] = json.dumps(flags)
    data["explanation"] = json.dumps(explanation)
    data["recommended_route"] = choose_route()
    data["status"] = "Pending Approval" if flags else "Approved"
    data["reference"] = "TQI-" + uuid.uuid4().hex[:8].upper()
    data.pop("amount_eur")
    payment = Payment(**data)
    db.add(payment); db.commit(); db.refresh(payment)
    add_audit(db, payment.reference, "PAYMENT_CREATED", f"Risk={score}; flags={len(flags)}")
    return payment

@app.get("/api/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.get(Payment, payment_id)
    if not payment: raise HTTPException(404, "Payment not found")
    return payment

@app.post("/api/payments/{payment_id}/invoice")
async def upload_invoice(payment_id: int, invoice: UploadFile = File(...), db: Session = Depends(get_db)):
    payment = db.get(Payment, payment_id)
    if not payment: raise HTTPException(404, "Payment not found")
    if not invoice.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF invoice")
    raw = await invoice.read()
    if len(raw) > 8_000_000: raise HTTPException(413, "PDF must be smaller than 8 MB")
    try:
        doc = fitz.open(stream=raw, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
    except Exception:
        raise HTTPException(400, "Could not read this PDF")
    import re
    amounts = re.findall(r"(?<!\w)(?:€|EUR\s*)?([0-9][0-9,]*(?:\.\d{2})?)(?!\w)", text, re.I)
    expected = round(payment.amount, 2)
    matched = any(abs(float(x.replace(",","")) - expected) < 0.01 for x in amounts)
    payment.invoice_match = int(matched)
    data = {"amount_eur":as_eur(payment.amount,payment.currency), "is_new_beneficiary":payment.is_new_beneficiary,
            "country_risk":payment.country_risk, "invoice_match":payment.invoice_match,
            "corridor_failure_rate":payment.corridor_failure_rate, "transaction_frequency":payment.transaction_frequency}
    score, level, explanation = predict_risk(data)
    payment.risk_score, payment.risk_level = score, level
    flags = policy_flags({**data, "country":payment.country, "risk_score":score})
    payment.policy_flags, payment.explanation = json.dumps(flags), json.dumps(explanation)
    payment.status = "Pending Approval" if flags else "Approved"
    db.commit()
    add_audit(db, payment.reference, "INVOICE_VERIFIED", f"amount_match={matched}")
    return {"matched":matched, "extracted_text_preview":text[:1000], "risk_score":score,
            "risk_level":level, "policy_flags":flags}

@app.post("/api/payments/{payment_id}/approve", response_model=PaymentOut)
def approve(payment_id: int, db: Session = Depends(get_db)):
    p = db.get(Payment,payment_id)
    if not p: raise HTTPException(404,"Payment not found")
    if p.status not in ("Pending Approval","Approved"): raise HTTPException(409,"Payment cannot be approved in its current state")
    p.status = "Processing"; db.commit()
    add_audit(db,p.reference,"HUMAN_APPROVED","Demo approver action")
    p.status = "Settled"; db.commit()
    add_audit(db,p.reference,"PAYMENT_SETTLED","Simulated settlement; no money moved")
    return p

@app.post("/api/payments/{payment_id}/reject", response_model=PaymentOut)
def reject(payment_id: int, db: Session = Depends(get_db)):
    p = db.get(Payment,payment_id)
    if not p: raise HTTPException(404,"Payment not found")
    if p.status != "Pending Approval": raise HTTPException(409,"Only pending payments can be rejected")
    p.status = "Rejected"; db.commit()
    add_audit(db,p.reference,"PAYMENT_REJECTED","Demo approver action")
    return p

@app.post("/api/payments/{payment_id}/retry", response_model=PaymentOut)
def retry(payment_id: int, db: Session = Depends(get_db)):
    p = db.get(Payment,payment_id)
    if not p: raise HTTPException(404,"Payment not found")
    if p.status != "Failed": raise HTTPException(409,"Only failed payments can be retried")
    p.recommended_route = choose_route()
    p.status = "Settled"
    p.failure_reason = None
    db.commit()
    add_audit(db,p.reference,"EXCEPTION_RETRY","Simulated retry via "+p.recommended_route)
    return p

@app.get("/api/audit")
def audit(db: Session = Depends(get_db)):
    return [{"id":e.id,"payment_reference":e.payment_reference,"action":e.action,
             "details":e.details,"created_at":e.created_at.isoformat()} for e in db.query(AuditEvent).order_by(desc(AuditEvent.id)).limit(100)]

@app.post("/api/demo/seed")
def seed_demo(db: Session = Depends(get_db)):
    if db.query(Payment).count() == 0:
        samples = [
            dict(beneficiary="Northstar Components",country="DE",account_identifier="DE89370400440532013000",amount=12400,currency="EUR",purpose="Industrial components",is_new_beneficiary=False,country_risk=.08,invoice_match=True,corridor_failure_rate=.03,transaction_frequency=12),
            dict(beneficiary="Acme Global Ltd",country="US",account_identifier="US123456789",amount=52000,currency="USD",purpose="Software services",is_new_beneficiary=True,country_risk=.12,invoice_match=True,corridor_failure_rate=.04,transaction_frequency=2),
            dict(beneficiary="Orion Trading",country="SG",account_identifier="SG123456789",amount=8700,currency="EUR",purpose="Trade settlement",is_new_beneficiary=True,country_risk=.18,invoice_match=False,corridor_failure_rate=.22,transaction_frequency=1),
        ]
        for item in samples:
            data={**item,"amount_eur":as_eur(item["amount"],item["currency"])}
            score,level,exp=predict_risk(data); flags=policy_flags({**data,"risk_score":score})
            p=Payment(**{**item,"reference":"TQI-DEMO-"+str(len(db.query(Payment).all())+1),
                "risk_score":score,"risk_level":level,"policy_flags":json.dumps(flags),
                "explanation":json.dumps(exp),"recommended_route":choose_route(),
                "status":"Pending Approval" if flags else "Approved"})
            db.add(p); db.commit(); db.refresh(p)
            if p.reference.endswith("3"):
                p.status="Failed"; p.failure_reason="Simulated intermediary corridor timeout"; db.commit()
            add_audit(db,p.reference,"DEMO_SEEDED","Synthetic demonstration transaction")
    return {"seeded":True,"count":db.query(Payment).count()}
