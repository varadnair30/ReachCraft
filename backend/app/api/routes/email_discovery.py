
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.scraping.email_discovery import EmailDiscoveryService
from app.models.email import EmailDiscoveryResult

router = APIRouter()

class EmailDiscoveryRequest(BaseModel):
    first_name: str
    last_name: str
    company: str
    company_domain: Optional[str] = None
    linkedin_url: Optional[str] = None

@router.post('/discover', response_model=EmailDiscoveryResult)
async def discover_email(request: EmailDiscoveryRequest):
    '''
    Discover email address for a person
    
    Example:
    ```
    {
      \"first_name\": \"John\",
      \"last_name\": \"Doe\",
      \"company\": \"Google\",
      \"company_domain\": \"google.com\"
    }
    ```
    '''
    try:
        service = EmailDiscoveryService()
        result = await service.discover_email(
            first_name=request.first_name,
            last_name=request.last_name,
            company=request.company,
            company_domain=request.company_domain,
            linkedin_url=request.linkedin_url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/health')
async def health():
    '''Health check for email discovery service'''
    return {'status': 'healthy', 'service': 'email_discovery'}
