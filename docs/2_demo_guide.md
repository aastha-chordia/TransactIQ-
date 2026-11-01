# TransactIQ — Platform Demonstration Guide

## 1. Launch the application
Complete the [Setup & Installation Guide](1_setup_guide.md), then open http://127.0.0.1:8000.

## 2. Load sample transactions
Click **Load demo data** on the dashboard. The demo endpoint creates three synthetic payment records if the database is empty. One record is marked as failed so the exception-retry workflow can be demonstrated.

## 3. Create a payment
Use the **Create payment request** form. Enter:
- Beneficiary and destination country
- Account identifier
- Amount and currency
- Payment purpose
- Country-risk estimate
- Corridor failure rate
- Transaction frequency
- Whether the beneficiary is new

Submit the form to receive a risk score, risk category, policy flags, recommended route, and initial status.

## 4. Review risk assessment
The Random Forest classifier estimates a risk probability using six transaction features. The service attempts to return SHAP feature contributions. If SHAP is unavailable or errors, it falls back to Random Forest feature-importance values. These are different explanation methods; identify the method accurately when presenting results.

## 5. Demonstrate invoice verification
The API accepts a PDF invoice at `POST /api/payments/{payment_id}/invoice`. Use a text-based PDF containing the expected amount. The current implementation extracts PDF text and checks whether the payment amount appears in that text. It does not perform OCR on scanned image-only PDFs.

## 6. Demonstrate approval and rejection
Payments with policy flags enter **Pending Approval**. Use the dashboard's Approve or Reject actions. Approval changes the record through simulated processing to Settled. No funds are transferred.

## 7. Demonstrate exception handling
The seeded failed record displays **Diagnose & retry**. The retry endpoint updates the simulated status and writes an audit event. This is a demonstration workflow, not a real bank or correspondent-bank retry.

## 8. Review audit events
Recent audit events appear on the dashboard. The complete recent event list is available through `GET /api/audit`.

## 9. Explore the API
Open http://127.0.0.1:8000/docs for interactive FastAPI documentation.

## Main API endpoints
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

## Notes for the demonstration
- Use text-based PDFs for invoice extraction; scanned PDFs are not OCR-processed.
- Invoice matching currently checks for the amount in extracted text; it is not a complete invoice validation engine.
- The restricted-country list is a small hard-coded demonstration list, not a live sanctions database.
- Currency conversion and payment-provider values are fixed illustrative values.
- The ML model uses synthetic data. Do not present synthetic results as proven real-world accuracy.
