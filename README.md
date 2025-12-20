# ReachCraft 🚀

> AI-powered job application automation that turns cold emails into warm conversations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)

## 🎯 Problem Statement

Job seekers send 200+ applications before landing an offer, with cold applications having only a **0.1-2% success rate**. However, **sourced candidates who reach out directly are 5x more likely to get hired**. The challenge? Personalizing hundreds of cold emails is impossible while juggling interviews, daily responsibilities, and job search stress.

Existing tools (Hunter.io `$49/month`, Apollo.io `$79/month`) are expensive and rely on paid APIs. **ReachCraft is 100% free, open-source, and built for job seekers by a job seeker.**

## ✨ Features

### 🤖 AI-Powered Personalization ✅ LIVE
- **Resume-driven email generation** that adapts to each role's requirements
- **Role-specific "I KNOW WHAT YOU WANT" sections** (defense autonomy ≠ fintech backend ≠ AI/ML)
- **Dynamic intro paragraphs** that highlight relevant experience per job description
- **Non-cliché subject line generation** using Gemini Flash 1.5
- **Anti-hallucination safeguards** with grounded resume facts
- **Simple web UI** for single-job email generation (batch queue coming soon)

### 🔍 Intelligent Email Discovery (Coming Week 2)
- Multi-source email finding (LinkedIn, company websites, GitHub)
- Pattern detection algorithms (firstname.lastname@company.com)
- Waterfall fallback system (local → Browserless → Bright Data)
- SMTP + DNS verification for 95%+ accuracy

### 📧 Smart Sending & Tracking (Coming Week 3)
- Dual email provider (Resend + SendGrid, 6,000 free emails/month)
- Intelligent rate limiting (avoid spam flags)
- Open/click tracking with analytics dashboard
- Auto follow-ups

### 🎨 Chrome Extension UI (Coming Week 4)
- Bulk upload via CSV or manual entry
- Real-time campaign progress tracking
- A/B testing for subject lines
- Analytics dashboard (response rates, best-performing emails)

## 🛠️ Tech Stack

**Frontend**: Simple HTML/CSS/JS (v1), React + TypeScript + TailwindCSS (planned)  
**Backend**: FastAPI, Python 3.10  
**Database**: Supabase (PostgreSQL) - schema created, persistence coming Week 2  
**AI/ML**: Gemini Flash 1.5  
**Scraping**: Playwright (planned), Browserless.io (planned)  
**Email**: Resend (planned), SendGrid (planned)  
**Queue/Cache**: Celery + Redis (planned)  
**Monitoring**: Sentry (planned), Langfuse (planned)  
**Deployment**: Local dev (current), Render + Vercel + Docker (planned)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Chrome browser
- Gemini API key (free tier: 1,500 requests/day)

### Installation

```bash
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

# Configure environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Run backend
uvicorn app.main:app --reload
# API docs: http://127.0.0.1:8000/docs

# In a separate terminal, run frontend (from ReachCraft/frontend)
python -m http.server 3000
# UI: http://localhost:3000
```

### Docker Setup (Coming Soon)

```bash
# From project root
docker-compose up
# Backend: http://localhost:8000
```

## 📊 Project Status

**Current Phase**: Week 1 Complete ✅ | Week 2 Starting 🚀  
**Progress**: AI email generation engine live with working UI

### Development Timeline
- [x] Week 0: Planning & Architecture
- [x] **Week 1: Backend Foundation + AI Email Generation**
  - [x] FastAPI backend with `/api/ai-generation/generate-complete` endpoint
  - [x] Resume-driven prompt builder with role adaptation
  - [x] Simple web UI for testing email generation
  - [x] Supabase database schema (campaigns, emails, contacts tables)
  - [x] Gemini Flash 1.5 integration
- [ ] Week 2: Database Persistence + Email Discovery
- [ ] Week 3: Email Sending + Tracking
- [ ] Week 4: Chrome Extension
- [ ] Week 5: Polish + Testing + Deployment
- [ ] Week 6: Demo Video + Portfolio Integration

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed weekly milestones.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Simple HTML/JS UI (v1)                │
│   [Chrome Extension coming Week 4]      │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│   FastAPI Backend                       │
│   - /api/ai-generation/generate-complete│
│   - Resume-driven prompt builder        │
└──┬────────────────────────────────────┬──┘
   │                                    │
   ▼                                    ▼
┌──────────────────┐         ┌──────────────────┐
│  Gemini Flash    │         │  Supabase        │
│  (AI Generation) │         │  (PostgreSQL)    │
└──────────────────┘         └──────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design.

## 💰 Cost

**Total: $0** (currently using only free tiers)

All services use free tiers:
- **Gemini Flash 1.5**: 1,500 requests/day (free forever)
- **Supabase**: 500MB PostgreSQL database (free forever)
- Resend: 3,000 emails/month (free) *[planned]*
- SendGrid: 3,000 emails/month (free) *[planned]*
- Render: 750 hours/month (free) *[planned]*
- Browserless: 5 hours/month (free) *[planned]*

## 📈 Impact Goals

- **50,000+ personalized emails** sent for job seekers
- **120% increase** in response rates vs generic applications
- **$0 cost** for users (no paid API dependencies)
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
- [Deployment Guide](docs/DEPLOYMENT.md) *[coming soon]*
- [Contributing Guidelines](CONTRIBUTING.md)

## 🐛 Known Issues

None yet! Report issues [here](https://github.com/varadnair30/ReachCraft/issues).

## 🗓️ Development Log

### Week 1 - Complete ✅ (December 14-20, 2025)
- ✅ Project scaffolding complete
- ✅ FastAPI backend initialized with `/api/ai-generation/generate-complete`
- ✅ Virtual environment configured
- ✅ Dependencies installed (FastAPI, Gemini SDK, Supabase client)
- ✅ Git repository initialized
- ✅ Supabase database schema created (campaigns, emails, contacts tables)
- ✅ Resume-driven prompt builder with role-specific adaptation
- ✅ Simple web UI for testing email generation
- ✅ Tested on defense autonomy, AI/ML, and backend roles
- 🔜 Next: Wire up database persistence + Email discovery pipeline (Week 2)

---

**⭐ Star this repo if you find it helpful!**
