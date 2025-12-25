from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.ai.gemini_service import GeminiService
from app.services.ai.prompt_builder import PromptBuilder
from app.core.supabase_client import get_supabase_client
from datetime import datetime, timedelta
import logging



logger = logging.getLogger(__name__)



router = APIRouter()



gemini = GeminiService()
supabase = get_supabase_client()



COMMON_TECH_KEYWORDS = [
    # Languages
    "python", "java", "javascript", "typescript", "go", "c++", "c#", "ruby", "rust",
    # Backend
    "fastapi", "django", "flask", "spring", "node.js", "express", "rails",
    # Frontend
    "react", "next.js", "vue", "angular", "svelte",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "dynamodb", "elasticsearch",
    # Cloud / Infra
    "aws", "gcp", "azure", "kubernetes", "docker", "terraform", "helm",
    "kafka", "rabbitmq", "grpc", "microservices", "serverless",
    # AI / Data
    "pandas", "numpy", "pytorch", "tensorflow", "llm", "rag", "spark",
    # DevOps / Others
    "ci/cd", "git", "github", "gitlab", "jenkins", "argo", "prometheus", "grafana"
]



def parse_job_description(job_description: str) -> dict:
    """
    Very simple parser:
    - Extracts tech stack keywords by scanning text
    - Uses first 2-3 sentences as a 'mission' summary fallback
    """
    if not job_description:
        return {"company_tech_stack": None, "company_mission": None}


    text_lower = job_description.lower()


    # Extract tech stack
    tech_found = []
    for tech in COMMON_TECH_KEYWORDS:
        # match tech word approximately
        if tech in text_lower:
            tech_found.append(tech.capitalize() if tech.islower() else tech)


    # De-duplicate while preserving order
    seen = set()
    tech_stack = []
    for t in tech_found:
        if t.lower() not in seen:
            tech_stack.append(t)
            seen.add(t.lower())


    # Very basic mission extraction: first 2-3 sentences
    import re
    sentences = re.split(r'(?<=[.!?])\s+', job_description.strip())
    mission = None
    if sentences:
        mission = " ".join(sentences[:2]).strip()


    return {
        "company_tech_stack": tech_stack or None,
        "company_mission": mission or None
    }




# Request Models - ENHANCED for Varad style
class SubjectLineRequest(BaseModel):
    recipient_first_name: str
    recipient_company: str
    recipient_title: Optional[str] = None
    sender_name: str
    sender_current_role: Optional[str] = None
    purpose: str = "job_inquiry"
    # NEW: Company research fields
    company_mission: Optional[str] = None
    role_name: Optional[str] = None



class CompleteEmailRequest(BaseModel):
    # Recipient info
    recipient_first_name: str
    recipient_last_name: Optional[str] = None
    recipient_company: str
    recipient_title: Optional[str] = None
    recipient_email: Optional[str] = None  # 🆕 For duplicate checking


    # Sender info (with defaults for Varad)
    sender_name: str = "Varad Nair"
    sender_email: Optional[str] = "vnairusa30@gmail.com"
    sender_phone: Optional[str] = "+1 (657)-767-9035"
    sender_background: Optional[str] = None
    sender_skills: Optional[List[str]] = []
    sender_portfolio: Optional[str] = "https://varadnair30.github.io/my_portfolio/"
    sender_linkedin: Optional[str] = "https://linkedin.com/in/varad-nair"
    sender_calendar: Optional[str] = "https://calendar.app.google/uLbvFdAuXgt4m41EA"


    # Job/Role context
    purpose: str = "job_inquiry"
    role_interested_in: Optional[str] = None
    role_url: Optional[str] = None



    # 🔹 NEW: Raw job description pasted from LinkedIn
    job_description: Optional[str] = Field(
        None,
        description="Full job description text pasted from LinkedIn"
    )


    # Company research - THE SECRET SAUCE
    company_mission: Optional[str] = Field(
        None,
        description="What the company actually builds/solves. If omitted and job_description is provided, it will be auto-derived."
    )
    company_tech_stack: Optional[List[str]] = Field(
        None,
        description="Specific technologies they use. If omitted and job_description is provided, it will be auto-derived."
    )
    company_notable_clients: Optional[List[str]] = Field(
        None,
        description="Big customers/users"
    )


    # Customization
    specific_passion_point: Optional[str] = Field(
        None,
        description="Why YOU care about this specific problem"
    )
    technical_hook: Optional[str] = Field(
        None,
        description="Specific technical challenge that excites you"
    )


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
    key_hook: Optional[str] = None
    email_id: Optional[str] = None  # 🆕 Supabase row ID
    duplicate_warning: Optional[str] = None  # 🆕 If already emailed this person



class EmailHistoryItem(BaseModel):
    id: str
    recipient_name: str
    recipient_email: Optional[str]
    recipient_company: str
    role_name: Optional[str]
    subject_line: str
    body: str
    created_at: str
    status: str



class EmailHistoryResponse(BaseModel):
    emails: List[EmailHistoryItem]
    total_count: int



@router.post("/generate-subject", response_model=SubjectLineResponse)
async def generate_subject_lines(request: SubjectLineRequest):
    """Generate killer subject lines in Varad's style - no generic BS"""
    try:
        logger.info(f"Generating Varad-style subject lines for {request.recipient_first_name} at {request.recipient_company}")


        prompt = PromptBuilder.build_subject_line_prompt(
            recipient_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_role=request.sender_current_role,
            purpose=request.purpose,
            company_mission=request.company_mission,
            role_name=request.role_name
        )


        logger.info(f"Calling Gemini API...")


        subject_lines = gemini.generate_subject_lines(prompt)


        logger.info(f"Generated {len(subject_lines)} killer subject lines")


        return SubjectLineResponse(
            subject_lines=subject_lines,
            primary=subject_lines[0] if subject_lines else "I Know What You're Building",
            metadata={
                "model": "gemini-2.5-flash",
                "purpose": request.purpose,
                "style": "varad_killer"
            }
        )


    except Exception as e:
        logger.error(f"Subject line generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/generate-complete", response_model=CompleteEmailResponse)
async def generate_complete_email(request: CompleteEmailRequest):
    """Generate a complete email in Varad's winning style"""
    try:
        logger.info(f"Generating Varad-style email for {request.recipient_first_name} at {request.recipient_company}")


        # 🆕 Check for duplicates if recipient_email is provided
        duplicate_warning = None
        if request.recipient_email:
            try:
                # Calculate 90 days ago (FIXED!)
                ninety_days_ago = (datetime.utcnow() - timedelta(days=90)).isoformat()

                result = supabase.table("emails").select("*").eq(
                    "recipient_email", request.recipient_email
                ).gte(
                    "created_at", ninety_days_ago  # ✅ Fixed: Check past 90 days, not future
                ).execute()


                if result.data and len(result.data) > 0:
                    last_email = result.data[0]
                    email_date = last_email['created_at'][:10]  # Just the date part
                    duplicate_warning = f"⚠️ You already emailed {request.recipient_email} on {email_date}"
                    logger.warning(duplicate_warning)
            except Exception as dup_err:
                logger.error(f"Duplicate check failed: {dup_err}")


        # 🔹 If job_description is provided, auto-derive mission/tech_stack when missing
        company_mission = request.company_mission
        company_tech_stack = request.company_tech_stack


        if request.job_description and (not company_mission or not company_tech_stack):
            parsed = parse_job_description(request.job_description)
            if not company_mission and parsed["company_mission"]:
                company_mission = parsed["company_mission"]
                logger.info("Derived company_mission from job_description")
            if not company_tech_stack and parsed["company_tech_stack"]:
                company_tech_stack = parsed["company_tech_stack"]
                logger.info(f"Derived tech stack from JD: {company_tech_stack}")


        # Build prompt with all the new context
        prompt = PromptBuilder.build_complete_email_prompt(
            recipient_first_name=request.recipient_first_name,
            recipient_last_name=request.recipient_last_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_email=request.sender_email,
            sender_phone=request.sender_phone,
            sender_background=request.sender_background,
            sender_skills=request.sender_skills,
            sender_portfolio=request.sender_portfolio,
            sender_linkedin=request.sender_linkedin,
            sender_calendar=request.sender_calendar,
            purpose=request.purpose,
            role_interested_in=request.role_interested_in,
            role_url=request.role_url,
            company_mission=company_mission,
            company_tech_stack=company_tech_stack,
            company_notable_clients=request.company_notable_clients,
            specific_passion_point=request.specific_passion_point,
            technical_hook=request.technical_hook,
            tone=request.tone
        )


        logger.info(f"Generating email body with Gemini (Varad style)...")


        # Generate email
        email_data = gemini.generate_json(prompt)


        logger.info(f"Email generated successfully")


        # Calculate metrics
        body = email_data.get('body', '')
        word_count = len(body.split())
        read_time = max(1, word_count // 200)
        confidence = gemini.calculate_confidence(body)
        key_hook = email_data.get('key_hook', '')


        # Generate subject variations
        logger.info(f"Generating subject variations...")


        subject_prompt = PromptBuilder.build_subject_line_prompt(
            recipient_name=request.recipient_first_name,
            recipient_company=request.recipient_company,
            recipient_title=request.recipient_title,
            sender_name=request.sender_name,
            sender_role=request.sender_background,
            purpose=request.purpose,
            company_mission=request.company_mission,
            role_name=request.role_interested_in
        )


        subject_variations = gemini.generate_subject_lines(subject_prompt)


        subject_line = email_data.get('subject', subject_variations[0])


        # 🆕 INSERT into Supabase
        email_id = None
        try:
            recipient_full_name = f"{request.recipient_first_name} {request.recipient_last_name or ''}".strip()


            insert_data = {
                "recipient_name": recipient_full_name,
                "recipient_email": request.recipient_email,
                "recipient_company": request.recipient_company,
                "recipient_title": request.recipient_title,
                "role_name": request.role_interested_in,
                "subject_line": subject_line,
                "body": body,
                "status": "generated",  # vs "sent" later
                "created_at": datetime.utcnow().isoformat()
            }


            result = supabase.table("emails").insert(insert_data).execute()


            if result.data:
                email_id = result.data[0].get('id')
                logger.info(f"✅ Email saved to Supabase with ID: {email_id}")
        except Exception as db_err:
            logger.error(f"Failed to save email to Supabase: {db_err}")
            # Don't fail the request, just log it


        logger.info(f"Complete! Word count: {word_count}, Key hook: {key_hook[:50] if key_hook else 'N/A'}...")


        return CompleteEmailResponse(
            subject_line=subject_line,
            body=body,
            confidence_score=confidence,
            subject_variations=subject_variations,
            word_count=word_count,
            estimated_read_time=read_time,
            key_hook=key_hook,
            email_id=email_id,
            duplicate_warning=duplicate_warning
        )


    except Exception as e:
        logger.error(f"Complete email generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/history", response_model=EmailHistoryResponse)
async def get_email_history(
    limit: int = 20,
    offset: int = 0,
    company: Optional[str] = None
):
    """
    Retrieve past generated emails


    Query params:
    - limit: Number of emails to return (default 20)
    - offset: Pagination offset (default 0)
    - company: Filter by company name (optional)
    """
    try:
        logger.info(f"Fetching email history (limit={limit}, offset={offset}, company={company})")


        query = supabase.table("emails").select("*", count="exact")


        # Filter by company if provided
        if company:
            query = query.ilike("recipient_company", f"%{company}%")


        # Order by most recent first
        query = query.order("created_at", desc=True)


        # Pagination
        query = query.range(offset, offset + limit - 1)


        result = query.execute()


        emails = [
            EmailHistoryItem(
                id=email["id"],
                recipient_name=email["recipient_name"],
                recipient_email=email.get("recipient_email"),
                recipient_company=email["recipient_company"],
                role_name=email.get("role_name"),
                subject_line=email["subject_line"],
                body=email["body"],
                created_at=email["created_at"],
                status=email.get("status", "generated")
            )
            for email in result.data
        ]


        total_count = result.count if result.count else len(emails)


        logger.info(f"Retrieved {len(emails)} emails (total: {total_count})")


        return EmailHistoryResponse(
            emails=emails,
            total_count=total_count
        )


    except Exception as e:
        logger.error(f"Failed to retrieve email history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))