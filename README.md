# ReachCraft 🚀

> AI-powered job application automation that turns cold emails into warm conversations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](https://reachcraft-frontend.onrender.com/)

**🌐 Live Application:** [https://reachcraft-frontend.onrender.com/](https://reachcraft-frontend.onrender.com/)  
**📚 API Docs:** [https://reachcraft.onrender.com/docs](https://reachcraft.onrender.com/docs)

---

## 🎯 Problem Statement

Job seekers send 200+ applications before landing an offer, with cold applications having only a **0.1-2% success rate**. However, **sourced candidates who reach out directly are 5x more likely to get hired**. The challenge? Personalizing hundreds of cold emails is impossible while juggling interviews, daily responsibilities, and job search stress.

Existing tools (Hunter.io `$49/month`, Apollo.io `$79/month`) are expensive and rely on paid APIs. **ReachCraft is 100% free, open-source, and built for job seekers by a job seeker.**

---

## ✨ Features

### 🤖 AI-Powered Email Generation ✅ LIVE IN PRODUCTION
- **Resume-driven email generation** that adapts to each role's requirements
- **Role-specific "I KNOW WHAT YOU WANT" sections** (defense autonomy ≠ fintech backend ≠ AI/ML)
- **Dynamic intro paragraphs** that highlight relevant experience per job description
- **Non-cliché subject line generation** using Gemini Flash 2.5
- **Anti-hallucination safeguards** with grounded resume facts
- **Database persistence** with Supabase (saves all generated emails)
- **Email history modal** to view and reuse past emails
- **Duplicate detection** (warns if you've already emailed someone in the past 90 days)

### 🔍 Email Discovery & Verification ✅ LIVE IN PRODUCTION
- **7-pattern email generation** (first.last@, first@, firstlast@, etc.)
- **SMTP verification** without paid APIs (checks if emails exist)
- **Confidence scoring** (0-100%) for each email candidate
- **MX record validation** and mailbox verification
- **Toggle SMTP verification** (instant pattern-only mode for speed)
- **Auto-save verified emails** to contacts database
- **Copy buttons** for quick email extraction

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

---

## 🛠️ Tech Stack

**Frontend**: HTML/CSS/JavaScript with responsive tab navigation  
**Backend**: FastAPI, Python 3.10.15  
**Database**: Supabase (PostgreSQL) with RLS policies  
**AI/ML**: Google Gemini Flash 2.5  
**Email Discovery**: dnspython (MX/SMTP verification)  
**Deployment**: Render (Backend Web Service + Static Site)  
**CI/CD**: GitHub auto-deploy on push to main  
**Queue/Cache**: Celery + Redis (planned)  
**Monitoring**: Sentry (planned), Langfuse (planned)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Supabase account (free tier)
- Gemini API key (free tier: 1,500 requests/day)

### Local Development

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
# Add your GEMINI_API_KEY, SUPABASE_URL, and SUPABASE_KEY to .env

# Run backend
uvicorn app.main:app --reload
# API docs: http://127.0.0.1:8000/docs

# In a separate terminal, run frontend (from ReachCraft/frontend)
python -m http.server 3000
# UI: http://localhost:3000
```

### Production Deployment

**Backend & Frontend are already deployed and live!**

- **Backend API:** [https://reachcraft.onrender.com](https://reachcraft.onrender.com)
- **Frontend UI:** [https://reachcraft-frontend.onrender.com/](https://reachcraft-frontend.onrender.com/)
- **Auto-Deploy:** Enabled via GitHub webhook (pushes to `main` trigger automatic redeploy)



---

## 📊 Database Setup

```sql
-- Run these SQL commands in Supabase SQL Editor

-- Emails table
CREATE TABLE emails (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  recipient_name TEXT NOT NULL,
  recipient_email TEXT,
  recipient_company TEXT NOT NULL,
  recipient_title TEXT,
  role_name TEXT,
  subject_line TEXT NOT NULL,
  body TEXT NOT NULL,
  status TEXT DEFAULT 'generated',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contacts table
CREATE TABLE contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT,
  email TEXT UNIQUE NOT NULL,
  company TEXT,
  title TEXT,
  confidence_score FLOAT DEFAULT 0.5,
  source TEXT,
  verified BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS and create policies (see docs/DATABASE.md for full setup)
```

---

## 📈 Project Status

**Current Phase**: Week 2 Complete ✅ | Deployed to Production 🚀 | Week 3 Starting  
**Progress**: AI email generation + Email discovery live with full UI in production

### Development Timeline
- [x] Week 0: Planning & Architecture
- [x] **Week 1: Backend Foundation + AI Email Generation**
  - [x] FastAPI backend with `/api/ai-generation/generate-complete` endpoint
  - [x] Resume-driven prompt builder with role adaptation
  - [x] Simple web UI for testing email generation
  - [x] Supabase database schema (campaigns, emails, contacts tables)
  - [x] Gemini Flash 1.5 integration
- [x] **Week 2: Database Persistence + Email Discovery + Production Deployment**
  - [x] Supabase persistence for all generated emails
  - [x] Email history endpoint with pagination (`GET /api/ai-generation/history`)
  - [x] Duplicate checking (90-day window with warnings)
  - [x] Email discovery service (7 pattern generation)
  - [x] SMTP verification without paid APIs
  - [x] Contacts database with confidence scoring
  - [x] Email Finder UI with tab navigation
  - [x] Copy buttons and "Find Another Email" workflow
  - [x] **Production deployment to Render**
  - [x] **CORS configuration for cross-origin requests**
  - [x] **CI/CD with automatic GitHub deploys**
- [ ] Week 3: Email Sending + Tracking
- [ ] Week 4: Chrome Extension
- [ ] Week 5: Polish + Testing + Advanced Features
- [ ] Week 6: Demo Video + Portfolio Integration



---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (Render Static Site)        │
│   HTML/JS UI with Tab Navigation       │
│   - Email Generator                     │
│   - Email Finder                        │
│   - History Modal                       │
└──────────────┬──────────────────────────┘
               │ HTTPS REST API (CORS enabled)
┌──────────────▼──────────────────────────┐
│   FastAPI Backend (Render Web Service) │
│   - /api/ai-generation/*                │
│   - /api/email-discovery/*              │
│   - Auto-deploy on Git push             │
└──┬────────────────────────────────────┬──┘
   │                                    │
   ▼                                    ▼
┌──────────────────┐         ┌──────────────────┐
│  Gemini Flash    │         │  Supabase        │
│  (AI Generation) │         │  (PostgreSQL)    │
│  dnspython       │         │  - emails        │
│  (SMTP Verify)   │         │  - contacts      │
└──────────────────┘         └──────────────────┘
```



---

## 💰 Cost

**Total: $0/month** (currently using only free tiers)

All services use free tiers:
- **Gemini Flash 1.5**: 1,500 requests/day (free forever)
- **Supabase**: 500MB PostgreSQL database (free forever)
- **dnspython**: Local SMTP verification (free forever)
- **Render**: Free tier for web service + static site
- Resend: 3,000 emails/month (free) *[planned]*
- SendGrid: 3,000 emails/month (free) *[planned]*

---

## 📈 Impact Goals

- **200+ personalized emails** generated for my job search
- **3+ interviews** landed from cold outreach
- **120% increase** in response rates vs generic applications
- **$0 cost** (no paid API dependencies)
- **100+ GitHub stars** (help other job seekers!)
- **Production-ready deployment** with CI/CD ✅

---

## 🤝 Contributing

This project is open-source to help job seekers worldwide. Contributions welcome!



---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Varad Nair**  
MS Computer Science @ UT Arlington | 4+ years experience in Full-Stack + Cloud + AI/ML  
[Portfolio](https://varadnair30.github.io/my_portfolio/) | [LinkedIn](https://linkedin.com/in/varad-nair) | [GitHub](https://github.com/varadnair30)

---

**Built with ❤️ by a job seeker, for job seekers**

*"Sourced candidates are 5x more likely to get hired. Let's automate the outreach, not the authenticity."*

---



## 🐛 Known Issues

### SMTP Verification Timeout in Production
**Issue:** Email discovery SMTP verification times out on Render's free tier (returns 20% confidence for all emails).

**Cause:** Render blocks outbound SMTP connections on port 25 for security/spam prevention.

**Workaround:** 
- **Local development:** SMTP verification works perfectly (use `uvicorn app.main:app --reload`)
- **Production:** Uncheck "Verify emails via SMTP" checkbox for instant pattern-based results (60-85% confidence)
- **Alternative:** Use paid Render plan ($7/month) or deploy to a platform that allows SMTP (AWS, GCP, DigitalOcean)

**Status:** This is a platform limitation, not a bug in ReachCraft. The app works as designed locally.

Report issues [here](https://github.com/varadnair30/ReachCraft/issues).

---

## 🗓️ Development Log

### Week 2.5 - Production Deployment ✅ (December 26, 2025)
- ✅ Backend deployed to Render Web Service
- ✅ Frontend deployed to Render Static Site
- ✅ Fixed Python version compatibility (3.10.15 for pydantic 2.5.3)
- ✅ Configured CORS middleware for cross-origin requests
- ✅ Set up CI/CD with automatic GitHub deployments
- ✅ Environment variable management in production
- ✅ Production testing and validation
- **Status: FULLY DEPLOYED AND LIVE** 🎉

### Week 2 - Complete ✅ (December 21-25, 2025)
- ✅ Supabase persistence integrated (`emails` and `contacts` tables)
- ✅ Email history API endpoint with pagination (`GET /api/ai-generation/history`)
- ✅ History modal UI (view past 50 emails, click to reload)
- ✅ Duplicate detection (warns if emailed same person within 90 days)
- ✅ Email discovery service with 7 pattern generation
- ✅ SMTP verification (dnspython, no paid APIs)
- ✅ Confidence scoring (0-100%) for email candidates
- ✅ Email Finder tab with results display
- ✅ Copy buttons for all email candidates
- ✅ "Find Another Email" workflow (no page reload)
- ✅ Color-coded confidence scores (green/yellow/red)
- 🔜 Next: Email sending with Resend/SendGrid + tracking (Week 3)

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



---

**⭐ Star this repo if you find it helpful!**

---

## 🎯 Portfolio Integration

**For Hiring Managers:**

This project demonstrates:
- ✅ **Full-stack development** (FastAPI backend, responsive frontend, PostgreSQL database)
- ✅ **AI/ML integration** (Gemini API, prompt engineering, anti-hallucination)
- ✅ **System design** (REST APIs, database schema, async processing)
- ✅ **DevOps & Deployment** (Render deployment, CI/CD, CORS, environment management)
- ✅ **Problem-solving** (free SMTP verification vs $49/month paid tools, Python version conflicts)
- ✅ **Shipping ability** (end-to-end working product deployed to production in 2 weeks)

**Real-world results:**
- ✅ Fully deployed production application
- ✅ 200+ personalized emails capable of being generated
- ✅ 0% operational cost (all free-tier services)
- ✅ Clean, production-ready code with proper error handling
- ✅ CI/CD pipeline with automatic deployments

**🌐 Try it yourself:** [https://reachcraft-frontend.onrender.com/](https://reachcraft-frontend.onrender.com/)

---

## 🚀 Deployment Details

### Technology Stack (Production)
- **Platform**: Render (Web Service + Static Site)
- **Runtime**: Python 3.10.15
- **Framework**: FastAPI 0.109.0
- **Database**: Supabase (PostgreSQL)
- **AI Model**: Google Gemini Flash 1.5
- **CI/CD**: GitHub webhook auto-deploy

### Performance
- **Cold start**: ~5-10 seconds (free tier)
- **Response time**: <2 seconds for email generation
- **Uptime**: 24/7 (with free tier spin-down after 15 min inactivity)

### Security
- CORS configured for production domains
- Environment variables managed via Render dashboard
- Supabase RLS policies for database security
- API key authentication for Gemini

### Known Limitations (Free Tier)
- **SMTP Verification**: Blocked on Render free tier (port 25 restricted). Use local development for full SMTP verification, or uncheck the verification option in production for pattern-based email discovery.
- **Cold start**: ~5-10 seconds after 15 minutes of inactivity
- **Uptime**: 24/7 with free tier spin-down


---

**Made with 💪 determination and ☕ coffee during an active job search**
