# TransactIQ — Setup & Installation Guide

## Prerequisites
- Python 3.10 or newer
- VS Code or another code editor
- Git (optional)

## Clone the repository
```bash
git clone https://github.com/aastha-chordia/TransactIQ-.git
cd TransactIQ-
```

## Create a virtual environment

**Windows PowerShell**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies and train the model
```bash
pip install -r requirements.txt
python ml/train_model.py
```

The training script generates reproducible synthetic transaction data and saves the Random Forest model under `ml_models/`. The API can also train the model automatically if the model file is missing.

## Start the application
Run this command from the repository root:
```bash
uvicorn app.main:app --reload
```

Open the following addresses:
- Dashboard: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## Run tests
```bash
pytest -q
```

## Configuration
The optional `DATABASE_URL` environment variable controls the SQLAlchemy database connection. By default, the project uses a local SQLite database named `transactiq.db`.

## Prototype limitations
TransactIQ is an academic simulator. It does not connect to SWIFT, real banks, live sanctions services, live foreign-exchange rates, or real payment networks. Provider values, currency conversion rates, and country restrictions are illustrative only. Do not use it for real financial or compliance decisions.
