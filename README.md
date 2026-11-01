# TransactIQ
**AI-Powered Cross-Border Payment Intelligence Platform**

TransactIQ is an educational FinTech prototype for cross-border payment operations. It demonstrates payment intake, invoice text extraction, ML risk scoring, explainability, policy holds, human approvals, route recommendations, exception diagnosis, and audit history.

> **Important:** This is a simulator. It does not connect to SWIFT, banks, live sanctions lists, foreign-exchange markets, or real money. Risk predictions are based on synthetic training data and must not be used for real financial decisions.

## Features
- Create and list international payment requests
- Extract invoice fields from text-based PDF invoices with PyMuPDF
- Random Forest risk prediction trained on generated synthetic data
- SHAP feature contributions when SHAP is installed and supported
- Deterministic safeguards for high-value payments, invoice mismatches, and restricted destinations
- Human approval workflow
- Provider ranking by cost, speed, and reliability
- Failed-payment diagnosis and simulated retry
- SQLite persistence and append-only audit event records
- Interactive browser dashboard

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python ml/train_model.py
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

The application automatically creates its SQLite database and trains a model if no model file exists.

## Demo workflow
1. Create a payment from the dashboard.
2. Upload a text-based PDF invoice to verify amount/currency.
3. Review risk score, explanations, policy flags, and recommended provider.
4. Approve a payment if it is held for review.
5. Use the seeded failed transaction to demonstrate exception diagnosis and retry.
6. Inspect the audit log.

## API overview
- `GET /api/dashboard`
- `GET /api/payments`
- `POST /api/payments`
- `GET /api/payments/{payment_id}`
- `POST /api/payments/{payment_id}/invoice`
- `POST /api/payments/{payment_id}/approve`
- `POST /api/payments/{payment_id}/reject`
- `POST /api/payments/{payment_id}/retry`
- `GET /api/audit`

Interactive OpenAPI documentation is available at `/docs`.

## Model
A Random Forest classifier is trained on reproducible synthetic transactions. Features include amount, new-beneficiary indicator, country-risk score, invoice match, corridor failure rate, and transaction frequency. The model output is a risk probability mapped to a 0–100 score. SHAP is used to provide local feature attributions where available.

Synthetic performance metrics are not evidence of real-world accuracy. A production system would require legally approved data, independent validation, calibration, fairness testing, robust monitoring, and human governance.

## Deployment
For a simple Render deployment:
- Build command: `pip install -r requirements.txt && python ml/train_model.py`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Use a persistent disk or managed database for durable production-like storage. The default SQLite database is suitable for local demos only.

## License
MIT
