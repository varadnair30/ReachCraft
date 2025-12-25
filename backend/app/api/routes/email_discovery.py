"""
Email Discovery API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.email_discovery import EmailDiscoveryService
from app.core.supabase_client import get_supabase_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services lazily (not at import time)
email_discovery = EmailDiscoveryService()


# Request Models
class EmailDiscoveryRequest(BaseModel):
    first_name: str = Field(..., description="Person's first name")
    last_name: str = Field(..., description="Person's last name")
    company_domain: str = Field(..., description="Company domain (e.g., 'twitch.tv')")
    company_name: Optional[str] = Field(None, description="Company name (for storage)")
    title: Optional[str] = Field(None, description="Person's job title")
    verify: bool = Field(True, description="Whether to verify emails via SMTP")
    save_to_db: bool = Field(True, description="Whether to save results to database")


# Response Models
class EmailCandidate(BaseModel):
    email: str
    pattern: str
    valid: Optional[bool]
    confidence: float
    reason: str


class EmailDiscoveryResponse(BaseModel):
    candidates: List[EmailCandidate]
    best_match: Optional[EmailCandidate]
    total_found: int


@router.post("/discover", response_model=EmailDiscoveryResponse)
async def discover_email(request: EmailDiscoveryRequest):
    """
    Discover email addresses for a person at a company

    Uses pattern generation + SMTP verification (no paid APIs)
    """
    try:
        logger.info(f"Discovering email for {request.first_name} {request.last_name} at {request.company_domain}")

        # Discover emails
        results = email_discovery.discover_email(
            first_name=request.first_name,
            last_name=request.last_name,
            company_domain=request.company_domain,
            verify=request.verify
        )

        # Convert to response model
        candidates = [
            EmailCandidate(
                email=r["email"],
                pattern=r["pattern"],
                valid=r.get("valid"),
                confidence=r["confidence"],
                reason=r["reason"]
            )
            for r in results
        ]

        # Best match is highest confidence
        best_match = candidates[0] if candidates else None

        # Save to database if requested
        if request.save_to_db and best_match and best_match.confidence >= 0.5:
            try:
                supabase = get_supabase_client()  # Get client only when needed

                insert_data = {
                    "first_name": request.first_name,
                    "last_name": request.last_name,
                    "email": best_match.email,
                    "company": request.company_name or request.company_domain,
                    "title": request.title,
                    "confidence_score": best_match.confidence,
                    "source": "pattern_smtp",
                    "verified": best_match.valid if best_match.valid is not None else False,
                    "created_at": datetime.utcnow().isoformat()
                }

                # Use upsert to avoid duplicates
                result = supabase.table("contacts").upsert(
                    insert_data,
                    on_conflict="email"
                ).execute()

                if result.data:
                    logger.info(f"✅ Saved contact to database: {best_match.email}")
            except Exception as db_err:
                logger.error(f"Failed to save contact: {db_err}")

        return EmailDiscoveryResponse(
            candidates=candidates,
            best_match=best_match,
            total_found=len(candidates)
        )

    except Exception as e:
        logger.error(f"Email discovery failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contacts", response_model=dict)
async def get_contacts(
    limit: int = 50,
    offset: int = 0,
    company: Optional[str] = None
):
    """
    Retrieve saved contacts from database
    """
    try:
        supabase = get_supabase_client()  # Get client only when needed

        query = supabase.table("contacts").select("*", count="exact")

        if company:
            query = query.ilike("company", f"%{company}%")

        query = query.order("created_at", desc=True).range(offset, offset + limit - 1)

        result = query.execute()

        return {
            "contacts": result.data,
            "total_count": result.count if result.count else len(result.data)
        }

    except Exception as e:
        logger.error(f"Failed to retrieve contacts: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))