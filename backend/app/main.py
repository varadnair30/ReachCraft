from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes.email_discovery import router as email_discovery_router
from app.api.routes.ai_generation import router as ai_generation_router

app = FastAPI(
    title='ReachCraft',
    description='AI-powered job application automation',
    version='0.1.0',
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:5173', 'chrome-extension://*', 'null'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers
app.include_router(
    email_discovery_router,
    prefix='/api/email-discovery',
    tags=['Email Discovery']
)

app.include_router(
    ai_generation_router,
    prefix='/api/ai-generation',
    tags=['AI Generation']
)

@app.get('/')
async def root():
    return {
        'message': 'ReachCraft API',
        'status': 'online',
        'version': '0.1.0',
        'endpoints': {
            'email_discovery': '/api/email-discovery',
            'ai_generation': '/api/ai-generation',
            'docs': '/docs'
        }
    }

@app.get('/health')
async def health():
    return {'status': 'healthy'}
