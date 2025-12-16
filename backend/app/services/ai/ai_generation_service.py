from typing import List, Dict, Any
from app.services.ai.gemini_service import GeminiService
from app.services.ai.prompts import (
    get_subject_prompt,
    get_body_prompt,
    get_complete_prompt
)
from app.models.ai_generation import (
    SubjectLineRequest,
    SubjectLineResponse,
    EmailBodyRequest,
    EmailBodyResponse,
    CompleteEmailRequest,
    CompleteEmailResponse
)

class AIGenerationService:
    '''Service for AI-powered email generation'''
    
    def __init__(self):
        self.gemini = GeminiService()
    
    async def generate_subject_lines(
        self,
        request: SubjectLineRequest
    ) -> SubjectLineResponse:
        '''Generate subject line variations'''
        
        # Build prompt
        prompt = get_subject_prompt(
            recipient_first_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title or 'Hiring Manager',
            sender_name=request.sender_name,
            sender_role=request.sender_current_role or 'Software Engineer',
            purpose=request.purpose,
            context=request.context
        )
        
        # Generate
        subject_lines = self.gemini.generate_subject_lines(prompt)
        
        # Pick primary (first one)
        primary = subject_lines[0] if subject_lines else 'Following up on our conversation'
        
        return SubjectLineResponse(
            subject_lines=subject_lines,
            primary=primary,
            metadata={
                'model': 'gemini-1.5-flash',
                'purpose': request.purpose
            }
        )
    
    async def generate_email_body(
        self,
        request: EmailBodyRequest
    ) -> EmailBodyResponse:
        '''Generate email body'''
        
        # Build prompt
        prompt = get_body_prompt(
            recipient_first_name=request.recipient_first_name,
            recipient_last_name=request.recipient_last_name or '',
            recipient_title=request.recipient_title or 'Hiring Manager',
            recipient_company=request.recipient_company,
            sender_name=request.sender_name,
            sender_background=request.sender_background,
            sender_skills=request.sender_skills,
            purpose=request.purpose,
            role_interested_in=request.role_interested_in,
            context=request.context,
            tone=request.tone
        )
        
        # Generate
        body = self.gemini.generate(prompt)
        
        # Calculate metrics
        word_count = len(body.split())
        estimated_read_time = int((word_count / 200) * 60)  # seconds (avg 200 wpm)
        
        return EmailBodyResponse(
            body=body.strip(),
            word_count=word_count,
            estimated_read_time=estimated_read_time,
            metadata={
                'model': 'gemini-1.5-flash',
                'tone': request.tone,
                'purpose': request.purpose
            }
        )
    
    async def generate_complete_email(
        self,
        request: CompleteEmailRequest
    ) -> CompleteEmailResponse:
        '''Generate complete email (subject + body)'''
        
        # Build prompt
        prompt = get_complete_prompt(
            recipient_first_name=request.recipient_first_name,
            recipient_last_name=request.recipient_last_name or '',
            recipient_title=request.recipient_title or 'Hiring Manager',
            recipient_company=request.recipient_company,
            sender_name=request.sender_name,
            sender_email=request.sender_email,
            sender_background=request.sender_background,
            sender_skills=request.sender_skills,
            sender_portfolio=request.sender_portfolio,
            sender_linkedin=request.sender_linkedin,
            role_interested_in=request.role_interested_in,
            context=request.context,
            tone=request.tone
        )
        
        # Generate
        result = self.gemini.generate_json(prompt)
        
        subject = result.get('subject', 'Following up')
        body = result.get('body', '').strip()
        
        # Generate variations for subject
        subject_request = SubjectLineRequest(
            recipient_first_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_current_role=None,
            purpose=request.purpose,
            context=request.context
        )
        
        subject_response = await self.generate_subject_lines(subject_request)
        
        # Calculate metrics
        word_count = len(body.split())
        estimated_read_time = int((word_count / 200) * 60)
        preview_text = body[:50] + '...' if len(body) > 50 else body
        confidence = self.gemini.calculate_confidence(body)
        
        return CompleteEmailResponse(
            subject_line=subject,
            subject_variations=subject_response.subject_lines,
            body=body,
            preview_text=preview_text,
            word_count=word_count,
            estimated_read_time=estimated_read_time,
            confidence_score=confidence,
            metadata={
                'model': 'gemini-1.5-flash',
                'tone': request.tone,
                'purpose': request.purpose
            }
        )
