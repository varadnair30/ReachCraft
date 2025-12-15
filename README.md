
# ReachCraft 🚀

> AI-powered job application automation that turns cold emails into warm conversations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)

## 🎯 Problem Statement

Job seekers send 200+ applications before landing an offer, with cold applications having only a **0.1-2% success rate**. However, **sourced candidates who reach out directly are 5x more likely to get hired**. The challenge? Personalizing hundreds of cold emails is impossible while juggling interviews, daily responsibilities, and job search stress.

Existing tools (Hunter.io \`\$49/month\`, Apollo.io \`\$79/month\`) are expensive and rely on paid APIs. **ReachCraft is 100% free, open-source, and built for job seekers by a job seeker.**

## ✨ Features

### 🔍 Intelligent Email Discovery
- Multi-source email finding (LinkedIn, company websites, GitHub)
- Pattern detection algorithms (firstname.lastname@company.com)
- Waterfall fallback system (local → Browserless → Bright Data)
- SMTP + DNS verification for 95%+ accuracy

### 🤖 AI-Powered Personalization
- Non-cliche subject line generation (Gemini Flash 1.5)
- RAG-enhanced email bodies (FAISS + LangChain)
- Context-aware personalization (company news, recipient background)
- Anti-hallucination safeguards

### 📧 Smart Sending & Tracking
- Dual email provider (Resend + SendGrid, 6,000 free emails/month)
- Intelligent rate limiting (avoid spam flags)
- Open/click tracking with analytics dashboard
- Auto follow-ups (coming soon)

### 🎨 Chrome Extension UI
- Bulk upload via CSV or manual entry
- Real-time campaign progress tracking
- A/B testing for subject lines
- Analytics dashboard (response rates, best-performing emails)

## 🛠️ Tech Stack

**Frontend**: React 18, TypeScript, Vite, TailwindCSS, React Query  
**Backend**: FastAPI, Python 3.10, Celery, Redis  
**Database**: Supabase (PostgreSQL 15 + Auth + Real-time)  
**AI/ML**: Gemini Flash, LangChain, FAISS, sentence-transformers  
**Scraping**: Playwright, Browserless.io, Bright Data  
**Email**: Resend, SendGrid, ZeroBounce  
**Monitoring**: Sentry, Langfuse  
**Deployment**: Render (backend), Vercel (landing page), Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- Chrome browser

### Installation

\`\`\`bash
# Clone repository
git clone https://github.com/varadnair30/ReachCraft.git
cd ReachCraft

# Backend setup
cd backend
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn app.main:app --reload
# Visit: http://127.0.0.1:8000
\`\`\`

### Docker Setup (Alternative)

\`\`\`bash
# From project root
docker-compose up
# Backend: http://localhost:8000
\`\`\`

## 📊 Project Status

**Current Phase**: Week 1 - Backend Foundation + Email Discovery  
**Progress**: 🔨 Infrastructure setup complete

### Development Timeline
- [x] Week 0: Planning & Architecture
- [ ] Week 1: Backend Foundation + Email Discovery
- [ ] Week 2: AI Personalization + RAG
- [ ] Week 3: Email Sending + Tracking
- [ ] Week 4: Chrome Extension
- [ ] Week 5: Polish + Testing + Deployment
- [ ] Week 6: Demo Video + Portfolio Integration

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed weekly milestones.

## 🏗️ Architecture

\`\`\`
┌─────────────────────────────────────────┐
│   Chrome Extension (React + TS)         │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│   FastAPI Backend + Celery Workers      │
└──┬────────┬──────────┬──────────────────┘
   │        │          │
   ▼        ▼          ▼
[Discovery][AI Gen][Email Send]
   │        │          │
   ▼        ▼          ▼
┌─────────────────────────────────────────┐
│  Supabase (PostgreSQL + Auth)           │
│  Upstash Redis (Cache + Queue)          │
└─────────────────────────────────────────┘
\`\`\`

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design.

## 💰 Cost

**Total: \$5 one-time** (Chrome Web Store developer fee)

All services use free tiers:
- Supabase: 500MB database (free forever)
- Gemini Flash: 1,500 requests/day (free forever)
- Resend: 3,000 emails/month (free)
- SendGrid: 3,000 emails/month (free)
- Render: 750 hours/month (free)
- Browserless: 5 hours/month (free)

## 📈 Impact Goals

- **50,000+ personalized emails** sent for job seekers
- **120% increase** in response rates vs generic applications
- **\$0 cost** for users (no paid API dependencies)
- **1,000+ GitHub stars** (help other job seekers!)

## 🤝 Contributing

This project is open-source to help job seekers worldwide. Contributions welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 👨‍💻 Author

**Varad Nair**  
MS Computer Science @ UT Arlington | 4+ years experience in Full-Stack + AI/ML  
[Portfolio](https://varadnair30.github.io/my_portfolio/) | [LinkedIn](https://linkedin.com/in/varad-nair) | [GitHub](https://github.com/varadnair30)

---

**Built with ❤️ by a job seeker, for job seekers**

*"Sourced candidates are 5x more likely to get hired. Let's automate the outreach, not the authenticity."*

---

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Development Roadmap](docs/ROADMAP.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🐛 Known Issues

None yet! This is Week 1. Report issues [here](https://github.com/varadnair30/ReachCraft/issues).

## 🗓️ Development Log

### Week 1 - Day 1 (December 14, 2025)
- ✅ Project scaffolding complete
- ✅ FastAPI backend initialized
- ✅ Virtual environment configured
- ✅ Dependencies installed
- ✅ Git repository initialized
- 🔜 Next: Supabase database setup

---

**⭐ Star this repo if you find it helpful!**
