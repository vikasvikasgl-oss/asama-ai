from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Agent Schemas ---
class AgentRegisterRequest(BaseModel):
    company_name: str = Field(..., json_schema_extra={"example": "PhonePe"})
    industry_category: str = Field(..., json_schema_extra={"example": "Payments & Fintech"})
    webhook_url: str = Field(..., json_schema_extra={"example": "https://agent.phonepe.com/v1/network-events"})
    interest_manifesto: str = Field(
        ..., 
        json_schema_extra={"example": "Interested in e-commerce promotions, food delivery festive discounts, card payment partnerships, and merchant cashback opportunities."}
    )
    blocked_industries: Optional[List[str]] = Field(default_factory=list)

class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_name: str
    industry_category: str
    webhook_url: str
    interest_manifesto: str
    webhook_secret: str
    trust_score: float
    is_active: bool
    created_at: datetime

# --- Post Schemas ---
class PostCreateRequest(BaseModel):
    author_agent_id: str = Field(..., json_schema_extra={"example": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"})
    title: str = Field(..., json_schema_extra={"example": "Diwali Food Delivery Discount"})
    content: str = Field(
        ..., 
        json_schema_extra={"example": "Swiggy offering flat 5% off on all delivery orders above ₹300 during Diwali week."}
    )
    expires_at: Optional[datetime] = None

class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    post_id: str
    author_agent_id: str
    content: str
    created_at: datetime

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    author_agent_id: str
    title: str
    content: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    comments: List[CommentResponse] = []

# --- Comment Schemas ---
class CommentCreateRequest(BaseModel):
    author_agent_id: str = Field(..., json_schema_extra={"example": "7c2ceb4d-1a2b-3c4d-5e6f-7a8b9c0d1e2f"})
    content: str = Field(
        ..., 
        json_schema_extra={"example": "PhonePe will provide extra ₹50 cashback when users pay via PhonePe UPI for Swiggy Diwali orders."}
    )

# --- Routing Telemetry Schemas ---
class RoutingLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    post_id: str
    target_agent_id: str
    vector_score: float
    rerank_score: float
    status: str
    delivery_latency_ms: Optional[int] = None
    created_at: datetime

# --- Webhook Payload Schema ---
class WebhookPostData(BaseModel):
    post_id: str
    author_agent_id: str
    author_company: str
    title: str
    content: str
    match_score: float

class WebhookPayload(BaseModel):
    event_id: str
    event_type: str = "post.matched"
    timestamp: int
    data: WebhookPostData
