from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PaymentCreate(BaseModel):
    beneficiary: str = Field(min_length=2, max_length=120)
    country: str = Field(min_length=2, max_length=2, description="ISO alpha-2 country code")
    account_identifier: str = Field(min_length=4, max_length=80)
    amount: float = Field(gt=0, le=100_000_000)
    currency: str = Field(min_length=3, max_length=3)
    purpose: str = Field(min_length=3, max_length=200)
    is_new_beneficiary: bool = False
    country_risk: float = Field(default=0.2, ge=0, le=1)
    invoice_match: bool = True
    corridor_failure_rate: float = Field(default=0.05, ge=0, le=1)
    transaction_frequency: int = Field(default=5, ge=0, le=10000)

class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    reference: str
    beneficiary: str
    country: str
    amount: float
    currency: str
    purpose: str
    risk_score: float
    risk_level: str
    status: str
    policy_flags: str
    explanation: str
    recommended_route: str
    failure_reason: Optional[str] = None
