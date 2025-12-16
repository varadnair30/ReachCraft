from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.ai.gemini_service import GeminiService
from app.services.ai.prompt_builder import PromptBuilder
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

gemini = GeminiService()

# Request Models
class SubjectLineRequest(BaseModel):
    recipient_first_name: str
    recipient_company: str
    recipient_title: Optional[str] = None
    sender_name: str
    sender_current_role: Optional[str] = None
    purpose: str = "job_inquiry"

class CompleteEmailRequest(BaseModel):
    recipient_first_name: str
    recipient_last_name: Optional[str] = None
    recipient_company: str
    recipient_title: Optional[str] = None
    sender_name: str
    sender_email: Optional[str] = None
    sender_background: Optional[str] = None
    sender_skills: Optional[List[str]] = []
    sender_portfolio: Optional[str] = None
    sender_linkedin: Optional[str] = None
    purpose: str = "job_inquiry"
    role_interested_in: Optional[str] = None
    tone: str = "professional"

# Response Models
class SubjectLineResponse(BaseModel):
    subject_lines: List[str]
    primary: str
    metadata: dict

class CompleteEmailResponse(BaseModel):
    subject_line: str
    body: str
    confidence_score: float
    subject_variations: List[str]
    word_count: int
    estimated_read_time: int

@router.post("/generate-subject", response_model=SubjectLineResponse)
async def generate_subject_lines(request: SubjectLineRequest):
    """Generate multiple subject line variations"""
    try:
        logger.info(f"Generating subject lines for {request.recipient_first_name} at {request.recipient_company}")
        
        prompt = PromptBuilder.build_subject_line_prompt(
            recipient_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_role=request.sender_current_role,
            purpose=request.purpose
        )
        
        logger.info(f"Calling Gemini API...")
        
        subject_lines = gemini.generate_subject_lines(prompt)
        
        logger.info(f"Generated {len(subject_lines)} subject lines")
        
        return SubjectLineResponse(
            subject_lines=subject_lines,
            primary=subject_lines[0] if subject_lines else "Following up on our conversation",
            metadata={
                "model": "gemini-2.5-flash",
                "purpose": request.purpose
            }
        )
    
    except Exception as e:
        logger.error(f"Subject line generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-complete", response_model=CompleteEmailResponse)
async def generate_complete_email(request: CompleteEmailRequest):
    """Generate a complete cold email with subject and body"""
    try:
        logger.info(f"Generating complete email for {request.recipient_first_name} at {request.recipient_company}")
        
        # Build prompt
        prompt = PromptBuilder.build_complete_email_prompt(
            recipient_first_name=request.recipient_first_name,
            recipient_last_name=request.recipient_last_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_email=request.sender_email,
            sender_background=request.sender_background,
            sender_skills=request.sender_skills,
            sender_portfolio=request.sender_portfolio,
            sender_linkedin=request.sender_linkedin,
            purpose=request.purpose,
            role_interested_in=request.role_interested_in,
            tone=request.tone
        )
        
        logger.info(f"Generating email body with Gemini...")
        
        # Generate email
        email_data = gemini.generate_json(prompt)
        
        logger.info(f"Email generated successfully")
        
        # Calculate metrics
        body = email_data.get('body', '')
        word_count = len(body.split())
        read_time = max(1, word_count // 200)
        confidence = gemini.calculate_confidence(body)
        
        # Generate subject variations
        logger.info(f"Generating subject variations...")
        
        subject_prompt = PromptBuilder.build_subject_line_prompt(
            recipient_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_role=request.sender_background,
            purpose=request.purpose
        )
        
        subject_variations = gemini.generate_subject_lines(subject_prompt)
        
        logger.info(f"Complete! Word count: {word_count}")
        
        return CompleteEmailResponse(
            subject_line=email_data.get('subject', subject_variations[0]),
            body=body,
            confidence_score=confidence,
            subject_variations=subject_variations,
            word_count=word_count,
            estimated_read_time=read_time
        )
    
    except Exception as e:
        logger.error(f"Complete email generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
