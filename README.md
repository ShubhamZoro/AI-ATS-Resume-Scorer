# AI ATS Resume Scorer

A full-stack web app that scores how well a resume matches a job description and returns deep, actionable feedback. Built with **FastAPI + Streamlit**, using spaCy and Sentence Transformers for NLP and the Groq API for LLM-generated improvement suggestions.

---

## What it does

1. **Upload** a resume (PDF or DOCX) and paste a job description.
2. The backend **parses** the resume, extracts skills, experience, education, projects, and contact info.
3. It **scores** the resume across five weighted categories and computes semantic similarity against the JD.
4. You get a **detailed report** — an overall ATS score, a per-category breakdown, detected issues with severity ratings, specific fix suggestions, and LLM-written improvement examples.
5. **Past analyses** are saved to your Supabase account so you can track progress over time.
6. Export a polished **PDF report** of any analysis.

---

## Score breakdown

| Category | Weight | What it measures |
|---|---|---|
| Formatting | 20% | Section headers, bullet structure, ATS-safe layout |
| Keywords | 25% | Overlap between resume terms and JD keywords |
| Content | 25% | Depth of experience, achievements, quantified results |
| Skill Validation | 15% | Skills in Skills section backed by evidence in experience/projects |
| ATS Compatibility | 15% | File format, no tables/images, standard fonts |

---

## Tech stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI (Python 3.11+) |
| **NLP** | spaCy `en_core_web_md` + Sentence Transformers `all-MiniLM-L6-v2` |
| **LLM** | Groq API (Llama 3) |
| **Auth + Database** | Supabase (email/password + Google OAuth) |
| **PDF Export** | WeasyPrint + Jinja2 |
| **File Parsing** | pdfplumber, PyPDF2, python-docx |

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | API info and endpoint listing |
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/analyze-resume` | Analyze a resume against a JD |
| `GET` | `/api/v1/history` | Get user's past analyses |
| `DELETE` | `/api/v1/history/{id}` | Delete a history entry |
| `POST` | `/api/v1/generate-pdf` | Generate a PDF report from analysis data |

Interactive docs available at `http://localhost:8000/docs` once the backend is running.

---

## Project structure

```
ATS_SCORER/
├── backend/
│   ├── api/
│   │   ├── routes.py          # All API route handlers
│   │   └── auth.py            # JWT token verification middleware
│   ├── core/
│   │   └── config.py          # All config, constants, and env loading
│   ├── models/
│   │   └── schemas.py         # Pydantic request/response models
│   ├── services/
│   │   ├── resume_parser.py   # File validation + text extraction (PDF/DOCX)
│   │   ├── resume_analyzer.py # Orchestrates the full analysis pipeline
│   │   ├── ats_scorer.py      # Scoring logic across all five categories
│   │   ├── jd_matcher.py      # JD keyword extraction + semantic matching
│   │   ├── feedback_engine.py # Issue detection with severity + fix suggestions
│   │   ├── recommendation_engine.py  # Groq LLM suggestion generation
│   │   ├── groq_parser.py     # Groq API client + structured output parsing
│   │   ├── report_generator.py       # Jinja2 HTML report builder
│   │   └── pdf_export.py      # WeasyPrint PDF generation
│   ├── database/              # Supabase DB interaction (history save/load)
│   ├── templates/             # Jinja2 HTML templates for PDF report
│   ├── utils/
│   │   └── file_utils.py      # Shared logging helpers, error types, fallback util
│   └── main.py                # FastAPI app entry point, model loading lifespan
│
├── frontend/
│   ├── views/
│   │   ├── landing.py         # Login / sign-up / OAuth page
│   │   ├── scorer.py          # Main upload + results view
│   │   ├── history.py         # Past analyses view
│   │   └── resources.py       # Tips and resources page
│   ├── components/            # Reusable UI components
│   ├── services/
│   │   └── supabase_client.py # Supabase auth client (email + Google OAuth)
│   ├── assets/                # Static images and icons
│   ├── .streamlit/
│   │   └── secrets.toml       # Streamlit secrets (not committed)
│   └── streamlit_app.py       # Streamlit entry point + routing
│
├── jupyterNotebook/           # EDA, dataset prep, model experiments (not required to run)
├── requirements.txt           # All backend + frontend dependencies
└── .env                       # Environment variables (not committed)
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/ShubhamZoro/AI-ATS-Resume-Scorer.git
cd "ATS Resume Scorer"

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

> **Windows users:** `python-magic-bin` is included in `requirements.txt` and bundles the required native DLL — no extra installation needed.

> **Linux users:** WeasyPrint requires system libraries:
> ```bash
> # Fedora
> sudo dnf install -y cairo pango gdk-pixbuf2 libffi
> # Debian / Ubuntu
> sudo apt install -y libcairo2 libpango-1.0-0 libpangoft2-1.0-0 libffi-dev
> ```

### 3. Configure environment variables

Create a `.env` file in the project root (and a copy at `backend/.env`):

```env
SUPABASE_URL="https://<your-project-ref>.supabase.co"
SUPABASE_KEY="<service_role key>"
SUPABASE_ANON_KEY="<anon / public key>"
SUPABASE_JWT_SECRET="<JWT secret>"
GROQ_API_KEY="<your Groq key>"
SENTENCE_TRANSFORMER_MODEL="all-MiniLM-L6-v2"
AUTH_REDIRECT_URL="http://127.0.0.1:8501"
```

Get Supabase keys from: **Project Settings → API** in your Supabase dashboard.
Get a Groq key from: [console.groq.com](https://console.groq.com)

### 4. Configure Streamlit secrets

Create `frontend/.streamlit/secrets.toml` with flat (un-sectioned) keys:

```toml
SUPABASE_URL = "https://<your-project-ref>.supabase.co"
SUPABASE_KEY = "<service_role key>"
SUPABASE_ANON_KEY = "<anon / public key>"
SUPABASE_JWT_SECRET = "<JWT secret>"
GROQ_API_KEY = "<your Groq key>"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
AUTH_REDIRECT_URL = "http://127.0.0.1:8501"
```

> ⚠️ Make sure `SUPABASE_ANON_KEY` and `SUPABASE_URL` belong to the **same** Supabase project — mismatching keys from different projects causes an `Invalid API key` error.

### 5. Run the backend

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API is live at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### 6. Run the frontend

In a second terminal (venv activated):

```bash
streamlit run frontend/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

App opens at `http://127.0.0.1:8501`.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Invalid API key` | `SUPABASE_ANON_KEY` in secrets.toml is from a different project | Replace with the anon key matching your `SUPABASE_URL` project |
| `failed to find libmagic` | `python-magic` requires native DLL not on Windows | Use `python-magic-bin` instead (already in `requirements.txt`) |
| `invalid syntax (feedback_engine.py, line 1)` | Stray non-Python text at top of file | Ensure line 1 is a `#` comment or import, not plain text |
| `Analysis pipeline failed` | spaCy model not downloaded | Run `python -m spacy download en_core_web_md` |
| Backend 422 on file upload | File too large or unsupported MIME type | Upload a PDF or DOCX under 5 MB |

---

## Notes

- **Never commit `.env` or `secrets.toml`** — they hold live API keys. Both are in `.gitignore`.
- The first run downloads the Sentence Transformer model (~90 MB). It's cached locally afterwards.
- If you don't have a Groq key, scoring still works — only the LLM-generated suggestions will be empty.
- `jupyterNotebook/` is for experimentation and is not required to run the app.
- Google OAuth requires setting the redirect URL (`http://127.0.0.1:8501`) as an allowed redirect in your Supabase dashboard under **Authentication → URL Configuration**.
