
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Campaign Model
class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: UUID
    user_id: UUID
    status: str = "draft"
    total_emails: int = 0
    sent_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    replied_count: int = 0
    failed_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Email Model
class EmailBase(BaseModel):
    recipient_email: EmailStr
    recipient_first_name: Optional[str] = None
    recipient_last_name: Optional[str] = None
    recipient_company: Optional[str] = None
    recipient_title: Optional[str] = None
    recipient_linkedin: Optional[str] = None

class EmailCreate(EmailBase):
    campaign_id: UUID

class EmailDiscoveryResult(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: Optional[str] = None  # 'linkedin', 'company_website', 'pattern', 'manual'
    confidence: float = 0.0
    verified: bool = False
    error: Optional[str] = None

class Email(EmailBase):
    id: UUID
    campaign_id: UUID
    subject_line: Optional[str] = None
    email_body: Optional[str] = None
    status: str = "pending"
    email_source: Optional[str] = None
    confidence_score: Optional[float] = None
    verified: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True