# TransactIQ
### AI-Powered Cross-Border Payment Intelligence Platform

TransactIQ is an AI-powered cross-border payment intelligence platform designed to demonstrate how machine learning, risk assessment, explainable AI, and intelligent payment routing can support international payment operations.

The platform provides a centralized interface to simulate payment processing, evaluate transaction risks, identify potential compliance concerns, recommend payment providers, manage approvals, and maintain transaction audit records.

---

## Project Links

| Parameter | Details |
|---|---|
| **GitHub Repository** | [TransactIQ Repository](https://github.com/aastha-chordia/TransactIQ-) |
| **Live Web Application** | [Open TransactIQ Dashboard](https://transactiq-ptbo.onrender.com/) |
| **Live API Backend** | [FastAPI Interactive Documentation](https://transactiq-ptbo.onrender.com/docs) |
| **API Health Check** | [Check Application Status](https://transactiq-ptbo.onrender.com/health) |

---

## Key Features

### 1. Payment Management
- Create and manage cross-border payment requests.
- View payment details and transaction status.
- Track payment information through a centralized dashboard.

### 2. AI-Based Risk Assessment
- Random Forest classification model for transaction risk prediction.
- Generates risk scores based on transaction characteristics.
- Evaluates factors such as transaction amount, beneficiary status, country risk, invoice matching, corridor failure rate, and transaction frequency.

### 3. Explainable AI (XAI)
- Provides explanations for risk predictions.
- Uses SHAP feature contributions when available and supported.
- Helps demonstrate which transaction attributes influence the model's risk assessment.

### 4. Compliance and Policy Checks
- Identifies potentially high-risk transactions.
- Applies deterministic policy checks for high-value payments, invoice mismatches, and restricted destinations.
- Supports human review and approval workflows.

### 5. Intelligent Payment Routing
- Recommends payment providers based on simulated cost, speed, and reliability characteristics.
- Compares available routing options to support payment decisions.

### 6. Invoice Verification
- Accepts text-based PDF invoices.
- Extracts relevant invoice information.
- Compares invoice details with payment information to identify mismatches.

### 7. Exception Management
- Demonstrates failed-payment diagnosis.
- Supports simulated payment retry workflows.
- Helps identify and manage transaction exceptions.

### 8. Audit Trail
- Maintains transaction-related audit events.
- Provides visibility into payment activities and approval actions.

---

## Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | Scikit-learn |
| ML Algorithm | Random Forest Classifier |
| Explainable AI | SHAP |
| Data Processing | NumPy, Pandas |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| PDF Processing | PyMuPDF |
| Deployment | Render |
| API Documentation | Swagger UI / OpenAPI |

---

## System Architecture

The platform follows a modular architecture consisting of a browser-based dashboard, FastAPI backend, machine learning service, database, and supporting business logic.

```text
             USER
               |
               v
       WEB DASHBOARD
       HTML / CSS / JS
               |
               v
        FASTAPI BACKEND
               |
       +-------+--------+
       |       |        |
       v       v        v
   PAYMENT    RISK    POLICY &
   SERVICE  ASSESSMENT COMPLIANCE
       |       |        |
       |       v        |
       |   RANDOM       |
       |   FOREST       |
       |   + SHAP       |
       |       |        |
       +-------+--------+
               |
               v
       PAYMENT ROUTING
       & EXCEPTION LOGIC
               |
               v
          SQLITE DB
               |
               v
          AUDIT LOG
```

---

## Project Structure

```text
TransactIQ/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   │
│   └── static/
│       └── index.html
│
├── ml/
│   └── train_model.py
│
├── ml_models/
│   └── .gitkeep
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Machine Learning Methodology

TransactIQ uses a Random Forest classification model to estimate the risk associated with a payment transaction.

### Model Input Features

The model considers the following transaction characteristics:

- Transaction amount
- New beneficiary indicator
- Country risk score
- Invoice match indicator
- Payment corridor failure rate
- Transaction frequency

### Risk Assessment Process

1. Payment information is submitted through the dashboard.
2. Transaction attributes are processed by the backend.
3. The Random Forest model estimates transaction risk.
4. The predicted probability is mapped to a risk score between 0 and 100.
5. Explainability information is generated using SHAP when available.
6. Policy checks identify transactions that may require additional review.
7. The system presents the risk assessment and relevant recommendations.

**Note:** The model is trained using synthetic transaction data for demonstration purposes. Its predictions are not validated for real-world financial decisions.

---

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code or another Python IDE

### Step 1: Clone the Repository

```bash
git clone https://github.com/aastha-chordia/TransactIQ-.git
```

### Step 2: Navigate to the Project Directory

```bash
cd TransactIQ-
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Train the Machine Learning Model

```bash
python ml/train_model.py
```

### Step 6: Start the Application

```bash
uvicorn app.main:app --reload
```

### Step 7: Open the Application

Dashboard:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

The application initializes its SQLite database and can train the model automatically if a trained model is not already available.

---

## API Endpoints

The FastAPI backend exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/api/dashboard` | Dashboard information |
| GET | `/api/payments` | Retrieve payment records |
| POST | `/api/payments` | Create a payment |
| GET | `/api/payments/{payment_id}` | Retrieve payment details |
| POST | `/api/payments/{payment_id}/invoice` | Upload and verify invoice |
| POST | `/api/payments/{payment_id}/approve` | Approve a payment |
| POST | `/api/payments/{payment_id}/reject` | Reject a payment |
| POST | `/api/payments/{payment_id}/retry` | Simulate payment retry |
| GET | `/api/audit` | Retrieve audit events |

Interactive API documentation:

[Open TransactIQ Swagger UI](https://transactiq-ptbo.onrender.com/docs)

---

## Demonstration Workflow

The following workflow can be used to explore the platform:

1. Open the TransactIQ dashboard.
2. Create a sample international payment.
3. Review the generated transaction risk score.
4. Examine the risk explanation and policy flags.
5. View the recommended payment provider.
6. Upload a sample text-based PDF invoice.
7. Review invoice matching results.
8. Demonstrate the human approval or rejection workflow.
9. Explore payment exception diagnosis and simulated retry.
10. Review the audit history.

---

## Deployment

TransactIQ is deployed using Render as a single web service.

**Live Application:**  
https://transactiq-ptbo.onrender.com/

**API Documentation:**  
https://transactiq-ptbo.onrender.com/docs

### Render Configuration

| Setting | Configuration |
|---|---|
| Service Type | Web Service |
| Runtime | Python 3 |
| Python Version | 3.11.11 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

The deployed application serves both the web dashboard and API through the same FastAPI service.

---

## Limitations and Future Scope

### Current Limitations

- The platform is an educational simulator and does not process real financial transactions.
- Payment provider characteristics, exchange rates, and routing outcomes are illustrative.
- The machine learning model uses synthetic transaction data.
- The platform does not integrate with live banking networks, SWIFT, real-time foreign exchange services, or live sanctions databases.
- Invoice extraction supports text-based PDFs and is not a complete OCR solution.
- The default SQLite database is intended for demonstration use. Render's free service does not provide persistent disk storage, so database records may not survive restarts or redeployments.

### Future Enhancements

- Integration with real payment gateways and banking APIs.
- Real-time foreign exchange rate integration.
- Advanced fraud detection using larger, validated datasets.
- OCR-based invoice processing.
- Enhanced explainability and model monitoring.
- Role-based access control and stronger authentication.
- Migration to PostgreSQL or another managed database.
- Persistent cloud storage and improved transaction monitoring.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**TransactIQ — Making Cross-Border Payment Intelligence Smarter, More Transparent, and More Explainable.**
