from sqlalchemy import Column, String, Text, TIMESTAMP, UUID, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.session import Base

"""
    Immutable audit trail for compliance and debugging.
    Captures who did what, when, and to which object.
"""

class AuditLog(Base):
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    actor = Column(String(255), nullable=False, index=True) 

    action = Column(String(100), nullable=False, index=True)

    object_type = Column(String(50), nullable=False, index=True) 
    
    object_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    payload = Column(JSONB, default=dict, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)