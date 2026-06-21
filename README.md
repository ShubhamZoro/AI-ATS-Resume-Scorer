# AI ATS Resume Scorer

> **Full-stack resume intelligence platform** — upload your resume, paste a job description, and get a detailed ATS compatibility score, evidence-backed skill validation, keyword gap analysis, LLM-generated fix suggestions, and a polished 4-page PDF export.

Built with **FastAPI + Streamlit**, powered by spaCy, Sentence Transformers, and the Groq API (Llama 3).

---

## ✨ Features

| Feature | Details |
|---|---|
| **ATS Scoring** | Five-category weighted score out of 100 |
| **Skill Validation** | Cross-checks skills section against project/experience evidence |
| **JD Matching** | Keyword overlap + semantic similarity via Sentence Transformers |
| **LLM Suggestions** | Groq-powered, concrete fix examples per issue |
| **PDF Export** | Professionally styled 4-report PDF (WeasyPrint / xhtml2pdf) |
| **History** | All past analyses saved to Supabase; view/delete anytime |
| **Auth** | Email/password + Google OAuth via Supabase |

---

## 📊 Scoring Breakdown

| Category | Weight | What it measures |
|---|---|---|
| Formatting | 20 pts | Section headers, bullet structure, ATS-safe layout |
| Keywords & Skills | 25 pts | Keyword overlap between resume and job description |
| Content Quality | 25 pts | Depth of experience, action verbs, quantified results |
| Skill Validation | 15 pts | Skills claimed in Skills section backed by project evidence |
| ATS Compatibility | 15 pts | File format, no tables/images, standard fonts, parse-friendly |

---

## 🗂️ PDF Report — 4 Pages

The exported PDF is a premium, colour-coded 4-report document:

| Report | Colour | Contents |
|---|---|---|
| **1 — Score Summary** | Navy / Blue | Overall score circle, per-category breakdown bars, strengths, critical issues |
| **2 — Skill Validation** | Teal / Green | Stats cards, validated skills with evidence badges, unvalidated skills, ATS compat table |
| **3 — JD Match Analysis** | Indigo / Purple | Keyword match %, semantic similarity %, matched/missing keyword pills, skills gap, suggestions |
| **4 — Recommendations** | Amber / Brown | All issues grouped by severity (High / Medium / Low) with fix boxes + printable checklist |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI (Python 3.11+) |
| **NLP** | spaCy `en_core_web_md` + Sentence Transformers `all-MiniLM-L6-v2` |
| **LLM** | Groq API (Llama 3) |
| **Auth + Database** | Supabase (email/password + Google OAuth) |
| **PDF Export** | WeasyPrint (preferred) with xhtml2pdf fallback |
| **Templating** | Jinja2 |
| **File Parsing** | pdfplumber, PyPDF2, python-docx |

---

## 📡 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | API info and endpoint listing |
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/analyze-resume` | Analyze a resume (PDF/DOCX) against a job description |
| `GET` | `/api/v1/history` | Retrieve the authenticated user's past analyses |
| `DELETE` | `/api/v1/history/{id}` | Delete a specific history entry |
| `POST` | `/api/v1/generate-pdf` | Generate a styled PDF report from analysis data |

Interactive Swagger docs: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
ATS Resume Scorer/
├── backend/
│   ├── api/
│   │   ├── routes.py                  # All API route handlers
│   │   └── auth.py                    # JWT token verification middleware
│   ├── core/
│   │   └── config.py                  # Config, constants, env loading
│   ├── models/
│   │   └── schemas.py                 # Pydantic request/response schemas
│   ├── services/
│   │   ├── resume_parser.py           # File validation + text extraction (PDF/DOCX)
│   │   ├── resume_analyzer.py         # Full analysis pipeline orchestrator
│   │   ├── ats_scorer.py              # Scoring logic across all five categories
│   │   ├── jd_matcher.py              # JD keyword extraction + semantic matching
│   │   ├── feedback_engine.py         # Issue detection with severity + fix suggestions
│   │   ├── recommendation_engine.py   # Groq LLM suggestion generation
│   │   ├── groq_parser.py             # Groq API client + structured output parsing
│   │   ├── report_generator.py        # Jinja2 context builder for HTML reports
│   │   └── pdf_export.py              # WeasyPrint / xhtml2pdf PDF generation
│   ├── database/                      # Supabase history save/load
│   ├── templates/                     # Jinja2 HTML templates for the 4-page PDF
│   │   ├── summary.html               # Report 1 — Score Summary
│   │   ├── action_items.html          # Report 2 — Skill Validation & Content
│   │   ├── quick_actions.html         # Report 3 — JD Match Analysis
│   │   └── jd_comparison.html         # Report 4 — Recommendations & Checklist
│   ├── utils/
│   │   └── file_utils.py              # Shared logging helpers, error types
│   └── main.py                        # FastAPI app entry point + model loading lifespan
│
├── frontend/
│   ├── views/
│   │   ├── landing.py                 # Login / sign-up / Google OAuth page
│   │   ├── scorer.py                  # Main upload + analysis results view
│   │   ├── history.py                 # Past analyses view
│   │   └── resources.py               # Tips and resume resources page
│   ├── components/                    # Reusable Streamlit UI components
│   ├── services/
│   │   └── supabase_client.py         # Supabase auth client (email + Google OAuth)
│   ├── assets/                        # Static images and icons
│   ├── .streamlit/
│   │   └── secrets.toml               # Streamlit secrets (not committed)
│   └── streamlit_app.py               # Streamlit entry point + page routing
│
├── jupyterNotebook/                   # EDA, dataset prep, model experiments (optional)
├── requirements.txt                   # All backend + frontend dependencies
└── .env                               # Environment variables (not committed)
```

---

## ⚙️ Setup

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

> **Windows users:** `python-magic-bin` is included in `requirements.txt` and bundles the required native DLL — no extra steps needed.

> **Linux users:** WeasyPrint requires system libraries:
> ```bash
> # Debian / Ubuntu
> sudo apt install -y libcairo2 libpango-1.0-0 libpangoft2-1.0-0 libffi-dev
>
> # Fedora
> sudo dnf install -y cairo pango gdk-pixbuf2 libffi
> ```

### 3. Configure environment variables

Create a `.env` file in the **project root** and a copy at `backend/.env`:

```env
SUPABASE_URL="https://<your-project-ref>.supabase.co"
SUPABASE_KEY="<service_role key>"
SUPABASE_ANON_KEY="<anon / public key>"
SUPABASE_JWT_SECRET="<JWT secret>"
GROQ_API_KEY="<your Groq key>"
SENTENCE_TRANSFORMER_MODEL="all-MiniLM-L6-v2"
AUTH_REDIRECT_URL="http://127.0.0.1:8501"
```

- Supabase keys → **Project Settings → API** in your Supabase dashboard
- Groq key → [console.groq.com](https://console.groq.com)

### 4. Configure Streamlit secrets

Create `frontend/.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://<your-project-ref>.supabase.co"
SUPABASE_KEY = "<service_role key>"
SUPABASE_ANON_KEY = "<anon / public key>"
SUPABASE_JWT_SECRET = "<JWT secret>"
GROQ_API_KEY = "<your Groq key>"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
AUTH_REDIRECT_URL = "http://127.0.0.1:8501"
```

> ⚠️ `SUPABASE_ANON_KEY` and `SUPABASE_URL` must belong to the **same** Supabase project. Mismatching keys from different projects causes an `Invalid API key` error.

### 5. Run the backend

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API live at `http://localhost:8000` · Swagger docs at `http://localhost:8000/docs`

### 6. Run the frontend

Open a **second terminal** (with venv activated):

```bash
streamlit run frontend/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

App opens at `http://127.0.0.1:8501`

---

## 🔧 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Invalid API key` | `SUPABASE_ANON_KEY` in secrets.toml is from a different project | Replace with the anon key matching your `SUPABASE_URL` project |
| `failed to find libmagic` | `python-magic` requires native DLL not found on Windows | `python-magic-bin` is already in `requirements.txt` — reinstall deps |
| `Analysis pipeline failed` | spaCy model not downloaded | Run `python -m spacy download en_core_web_md` |
| `Failed to generate PDF` | xhtml2pdf encountered unsupported CSS | Ensure templates only use xhtml2pdf-compatible CSS (no `:not()`, no CSS Grid) |
| Backend 422 on file upload | File too large or unsupported MIME type | Upload a PDF or DOCX under 5 MB |
| `invalid syntax` in service file | Stray non-Python text at top of file | Ensure line 1 is a `#` comment or import statement |

---

## 📝 Notes

- **Never commit `.env` or `secrets.toml`** — they contain live API keys. Both are already in `.gitignore`.
- The first run downloads the Sentence Transformer model (~90 MB). It is cached locally afterwards.
- If you don't have a Groq key, scoring still works — only LLM-generated fix examples will be absent.
- PDF export uses **WeasyPrint** when its native libraries are available, and falls back to **xhtml2pdf** (pure-Python, zero system dependencies) automatically.
- Google OAuth requires adding `http://127.0.0.1:8501` as an allowed redirect URL in Supabase under **Authentication → URL Configuration**.
- `jupyterNotebook/` contains EDA and model experiments and is **not required** to run the app.
