import uuid
import json
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_name = Column(String(255), nullable=False)
    industry_category = Column(String(100), nullable=False)
    webhook_url = Column(Text, nullable=False)
    interest_manifesto = Column(Text, nullable=False)
    interest_embedding = Column(Text, nullable=True)  # JSON-encoded float array
    webhook_secret = Column(String(255), nullable=False, default=generate_uuid)
    trust_score = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    blocked_industries = Column(Text, default="[]")  # JSON-encoded list of strings
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    routing_logs = relationship("RoutingLog", back_populates="target_agent", cascade="all, delete-orphan")

    def get_embedding(self) -> list[float]:
        if self.interest_embedding:
            return json.loads(self.interest_embedding)
        return []

    def set_embedding(self, emb: list[float]):
        self.interest_embedding = json.dumps(emb)

    def get_blocked_industries(self) -> list[str]:
        if self.blocked_industries:
            return json.loads(self.blocked_industries)
        return []

class Post(Base):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    author_agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    post_embedding = Column(Text, nullable=True)  # JSON-encoded float array
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    # Relationships
    author = relationship("Agent", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    routing_logs = relationship("RoutingLog", back_populates="post", cascade="all, delete-orphan")

    def get_embedding(self) -> list[float]:
        if self.post_embedding:
            return json.loads(self.post_embedding)
        return []

    def set_embedding(self, emb: list[float]):
        self.post_embedding = json.dumps(emb)

class RoutingLog(Base):
    __tablename__ = "routing_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(String(36), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    target_agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    vector_score = Column(Float, nullable=False)
    rerank_score = Column(Float, nullable=False)
    status = Column(String(50), default="NOTIFIED")  # NOTIFIED, ENGAGED, IGNORED, FAILED, DROPPED
    delivery_latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    post = relationship("Post", back_populates="routing_logs")
    target_agent = relationship("Agent", back_populates="routing_logs")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(String(36), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    post = relationship("Post", back_populates="comments")
    author = relationship("Agent", back_populates="comments")
