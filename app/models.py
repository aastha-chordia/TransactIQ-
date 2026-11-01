from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    beneficiary: Mapped[str] = mapped_column(String(120))
    country: Mapped[str] = mapped_column(String(2))
    account_identifier: Mapped[str] = mapped_column(String(80))
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3))
    purpose: Mapped[str] = mapped_column(String(200))
    is_new_beneficiary: Mapped[int] = mapped_column(Integer, default=0)
    country_risk: Mapped[float] = mapped_column(Float, default=0.2)
    invoice_match: Mapped[int] = mapped_column(Integer, default=1)
    corridor_failure_rate: Mapped[float] = mapped_column(Float, default=0.05)
    transaction_frequency: Mapped[int] = mapped_column(Integer, default=5)
    risk_score: Mapped[float] = mapped_column(Float, default=0)
    risk_level: Mapped[str] = mapped_column(String(20), default="Pending")
    status: Mapped[str] = mapped_column(String(30), default="Pending Approval")
    policy_flags: Mapped[str] = mapped_column(Text, default="[]")
    explanation: Mapped[str] = mapped_column(Text, default="[]")
    recommended_route: Mapped[str] = mapped_column(String(80), default="Provider Alpha")
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_reference: Mapped[str] = mapped_column(String(24), index=True)
    action: Mapped[str] = mapped_column(String(80))
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
