# TransactIQ — Detailed Project Documentation

## 1. Project overview
TransactIQ is an AI-assisted cross-border payment operations prototype. It combines payment intake, machine-learning risk estimation, invoice text extraction, deterministic policy checks, provider-route scoring, human review, simulated exception recovery, and audit events.

**System boundary:** TransactIQ is an academic simulator. It does not initiate or settle real payments and does not connect to SWIFT, banks, live sanctions services, or live FX feeds.

## 2. Problem context
Cross-border payments may involve multiple currencies, intermediary institutions, jurisdictions, and operational checks. Delays or exceptions can arise from incomplete payment information, document mismatches, corridor issues, or compliance review. TransactIQ models selected stages of this workflow for demonstration.

## 3. System modules

| Module | Technology | Responsibility |
|---|---|---|
| Payment intake | FastAPI, Pydantic | Validates and receives payment requests |
| Persistence | SQLAlchemy, SQLite | Stores payment records and audit events |
| Invoice extraction | PyMuPDF, regular expressions | Extracts text from text-based PDFs and checks for the payment amount |
| Risk prediction | Scikit-learn Random Forest | Estimates transaction risk from six input features |
| Explainability | SHAP with fallback | Attempts local feature contributions; falls back to model feature importance |
| Policy checks | Python rules | Flags high-value payments, invoice mismatches, selected country codes, and critical scores |
| Route recommendation | Weighted scoring | Selects among three illustrative providers |
| Approval workflow | FastAPI endpoints | Supports simulated approval and rejection |
| Exception retry | FastAPI endpoint | Simulates retry for failed records |
| Audit trail | SQLAlchemy | Records key payment workflow events |
| Dashboard | HTML, CSS, JavaScript | Displays metrics, transactions, actions, and audit events |

## 4. Machine-learning model

### Input features
1. Amount converted to approximate EUR using a fixed demonstration conversion table.
2. New-beneficiary indicator.
3. Country-risk estimate from 0 to 1.
4. Invoice-match indicator.
5. Corridor failure rate from 0 to 1.
6. Transaction frequency.

### Training process
The training script generates 3,500 reproducible synthetic records using NumPy. A Random Forest classifier is trained and saved using Joblib at `ml_models/risk_model.joblib`.

### Risk score
The classifier's positive-class probability is multiplied by 100 to produce a risk score. The application assigns the following categories:
- Low: below 30
- Medium: 30 to below 60
- High: 60 to below 85
- Critical: 85 and above

The synthetic dataset is for demonstrating the pipeline only. It is not representative of real banking fraud and has not established real-world model performance.

### Explainability
The service attempts to calculate SHAP values using TreeExplainer. If SHAP is unavailable or raises an exception, it returns Random Forest feature importances. Global feature importance is not equivalent to a local SHAP explanation, so the distinction should be made clear during evaluation.

## 5. Policy engine
The prototype flags:
- Payments above the EUR 25,000 equivalent threshold.
- Invoice amount mismatches.
- Destination country codes KP, IR, or SY.
- Critical model risk scores of 85 or higher.

Flagged payments are placed in Pending Approval. These are illustrative rules and are not a substitute for applicable laws, regulatory advice, or live sanctions screening.

## 6. Route recommendation
Three fictional payment providers are configured with illustrative fees, processing times, and reliability values. A weighted score combines these values, and the lowest-scoring provider is recommended. No provider APIs are contacted.

## 7. End-to-end workflow
1. A user submits a payment request.
2. Pydantic validates the submitted fields.
3. The ML service calculates a risk score and explanation.
4. The policy engine evaluates deterministic rules.
5. The route service recommends a provider.
6. The payment is stored as Pending Approval if flags exist, otherwise Approved.
7. A reviewer can approve or reject a pending request.
8. Failed demonstration records can be retried through the simulated retry endpoint.
9. Workflow actions are stored in the audit-event table.

## 8. Project structure
```text
TransactIQ/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   └── static/
│       └── index.html
├── docs/
│   ├── 1_setup_guide.md
│   ├── 2_demo_guide.md
│   └── 3_detailed_documentation.md
├── ml/
│   └── train_model.py
├── ml_models/
│   └── .gitkeep
├── tests/
│   └── test_api.py
├── requirements.txt
├── README.md
└── LICENSE
```

## 9. API reference
The interactive OpenAPI documentation is available at `/docs`. Main endpoints:
- `GET /health`
- `GET /api/dashboard`
- `GET /api/payments`
- `POST /api/payments`
- `GET /api/payments/{payment_id}`
- `POST /api/payments/{payment_id}/invoice`
- `POST /api/payments/{payment_id}/approve`
- `POST /api/payments/{payment_id}/reject`
- `POST /api/payments/{payment_id}/retry`
- `GET /api/audit`
- `POST /api/demo/seed`

## 10. Limitations and future enhancements
Current limitations include synthetic model data, no independent model validation, simplified invoice amount matching, no OCR for scanned invoices, fixed FX conversion values, illustrative provider parameters, a small hard-coded country list, simulated settlement, and basic API security.

Future work could include secure role-based access, OCR with document validation, authorized sanctions-data integration, validated training data, calibration and fairness evaluation, model-drift monitoring, database migrations, stronger audit integrity, and payment-provider sandbox integration.

## 11. Responsible-use statement
TransactIQ is an academic prototype for demonstrating AI concepts in banking operations. It is not a live payment service, regulatory compliance product, or financial decision-making system.
