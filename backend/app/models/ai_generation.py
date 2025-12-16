from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID

# Subject Line Generation
class SubjectLineRequest(BaseModel):
    recipient_first_name: str
    recipient_company: str
    recipient_title: Optional[str] = None
    sender_name: str
    sender_current_role: Optional[str] = None
    purpose: str = 'job_inquiry'  # 'job_inquiry', 'networking', 'referral'
    context: Optional[str] = None  # Additional context

class SubjectLineResponse(BaseModel):
    subject_lines: List[str] = Field(..., description='List of 3 subject line variations')
    primary: str = Field(..., description='Best subject line')
    metadata: dict = Field(default_factory=dict)

# Email Body Generation
class EmailBodyRequest(BaseModel):
    recipient_first_name: str
    recipient_last_name: Optional[str] = None
    recipient_company: str
    recipient_title: Optional[str] = None
    sender_name: str
    sender_background: str  # Brief background (e.g., '4 years full-stack experience')
    sender_skills: List[str]  # Key skills
    purpose: str = 'job_inquiry'
    role_interested_in: Optional[str] = None
    subject_line: Optional[str] = None
    context: Optional[str] = None
    tone: str = 'professional'  # 'professional', 'casual', 'enthusiastic'

class EmailBodyResponse(BaseModel):
    body: str
    word_count: int
    estimated_read_time: int  # seconds
    metadata: dict = Field(default_factory=dict)

# Complete Email Generation (Subject + Body)
class CompleteEmailRequest(BaseModel):
    recipient_first_name: str
    recipient_last_name: Optional[str] = None
    recipient_company: str
    recipient_title: Optional[str] = None
    recipient_linkedin: Optional[str] = None
    sender_name: str
    sender_email: EmailStr
    sender_background: str
    sender_skills: List[str]
    sender_portfolio: Optional[str] = None
    sender_linkedin: Optional[str] = None
    purpose: str = 'job_inquiry'
    role_interested_in: Optional[str] = None
    context: Optional[str] = None
    tone: str = 'professional'

class CompleteEmailResponse(BaseModel):
    subject_line: str
    subject_variations: List[str]
    body: str
    preview_text: str  # First 50 chars
    word_count: int
    estimated_read_time: int
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: dict = Field(default_factory=dict)
