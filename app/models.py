from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Department(str, Enum):
    billing = "billing"
    security = "security"
    technical_support = "technical_support"
    account_access = "account_access"
    product = "product"


class TicketRequest(BaseModel):
    subject: str = Field(..., min_length=3, max_length=160)
    message: str = Field(..., min_length=10, max_length=4000)
    customer_tier: str = Field("standard", pattern="^(standard|pro|enterprise)$")


class TicketClassification(BaseModel):
    priority: Priority
    department: Department
    confidence: float = Field(..., ge=0, le=1)
    tags: list[str]
    summary: str
    recommended_response: str
