# AI Resume Analyzer

[![Live Demo](https://img.shields.io/badge/demo-deploy-blue)](https://github.com/praah18/AI_Resume_Analyzer)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB)](https://react.dev/)

AI-powered resume analysis platform that scores ATS compatibility, extracts skills, and generates personalized feedback using **Sentence Transformers (BERT)**, **cosine similarity**, and **Google Gemini**.

![Dashboard Preview](docs/screenshots/dashboard.png)

> Add screenshots to `docs/screenshots/` after running locally (dashboard, analyze, results).

## Features

- **PDF resume upload** with drag-and-drop
- **Job description** paste/upload analysis
- **ATS compatibility score** (70% semantic + 30% keyword match)
- **BERT embeddings** via `all-MiniLM-L6-v2` + cosine similarity
- **Skill gap analysis** — matched vs missing skills
- **Gemini AI feedback** — strengths, weaknesses, ATS tips
- **Keyword optimization** suggestions
- **PDF report export**
- **JWT authentication** & user dashboard
- **Analysis history** with score charts
- **Dark / light mode**
- **Mobile responsive** UI

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 19, Vite, Tailwind CSS 4, Recharts, React Router |
| Backend | FastAPI, SQLAlchemy, SQLite, JWT |
| AI/NLP | Sentence Transformers, scikit-learn, Google Gemini API |
| Deploy | Vercel (frontend), Render/Railway (backend) |

## Project Structure

```
AI_Resume_Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Environment settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # User, Analysis ORM
│   │   ├── schemas/             # Pydantic DTOs
│   │   ├── routers/             # Auth & analysis APIs
│   │   ├── services/            # AI pipeline, PDF, skills
│   │   └── utils/               # JWT, logging
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/                 # Axios client
│   │   ├── components/          # Reusable UI
│   │   ├── context/             # Auth & theme
│   │   └── pages/               # Landing, dashboard, etc.
│   └── package.json
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set SECRET_KEY and GEMINI_API_KEY
python run.py
```

API runs at **http://localhost:8000**  
Docs: **http://localhost:8000/api/docs**

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Optional: VITE_API_URL=http://localhost:8000 (proxy works in dev)
npm run dev
```

App runs at **http://localhost:5173**

### 3. First Use

1. Open http://localhost:5173
2. **Register** a new account
3. Go to **Analyze** → upload PDF resume → paste job description
4. View ATS score, skills, AI feedback
5. **Download PDF** report

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | JWT signing secret (long random string) |
| `GEMINI_API_KEY` | Google Gemini API key |
| `DATABASE_URL` | Default: `sqlite:///./data/resume_analyzer.db` |
| `CORS_ORIGINS` | Comma-separated frontend URLs |
| `GEMINI_MODEL` | Default: `gemini-2.0-flash` |
| `EMBEDDING_MODEL` | Default: `all-MiniLM-L6-v2` |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Production backend URL (e.g. `https://your-api.onrender.com`) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| GET | `/api/auth/me` | Current user |
| POST | `/api/analysis/analyze` | Upload resume + analyze |
| GET | `/api/analysis/history` | User analysis history |
| GET | `/api/analysis/{id}` | Single analysis |
| GET | `/api/analysis/{id}/report` | Download PDF report |
| GET | `/api/health` | Health check |

## Deployment

### Frontend → Vercel

1. Import repo on [Vercel](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Build: `npm run build` · Output: `dist`
4. Environment: `VITE_API_URL=https://your-backend.onrender.com`

### Backend → Render

1. New **Web Service** on [Render](https://render.com)
2. Root: `backend` · Build: `pip install -r requirements.txt`
3. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set env vars from `.env.example`
5. Update `CORS_ORIGINS` with your Vercel URL

### Backend → Railway

Same as Render — point to `backend/`, set `PORT` and environment variables.

## Screenshots

Place captures in `docs/screenshots/`:

| Screenshot | File |
|------------|------|
| Landing page | `landing.png` |
| Dashboard | `dashboard.png` |
| Analyze flow | `analyze.png` |
| Results & charts | `results.png` |

## How ATS Scoring Works

1. **Extract text** from uploaded PDF
2. **Extract skills** from resume & job description (taxonomy + regex)
3. **BERT embeddings** — cosine similarity → semantic score (0–100%)
4. **Keyword match** — % of job skills found in resume
5. **ATS score** = `0.7 × semantic + 0.3 × keyword`
6. **Gemini** generates feedback, suggestions, and keywords

## License

MIT — portfolio and educational use.

## Author

**Prachi Rai** — [GitHub](https://github.com/praah18/AI_Resume_Analyzer)
