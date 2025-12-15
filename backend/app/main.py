
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.email_discovery import router as email_discovery_router

app = FastAPI(
    title='ReachCraft',
    description='AI-powered job application automation',
    version='0.1.0',
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:5173', 'chrome-extension://*'],
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

@app.get('/')
async def root():
    return {'message': 'ReachCraft API', 'status': 'online', 'version': '0.1.0'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}
