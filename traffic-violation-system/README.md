# AI-Based Smart Traffic Violation Detection System - Backend API

Production-ready FastAPI backend for logging, tracking, and managing traffic violations.

## 📂 Folder Structure

```text
traffic-violation-system/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/          # API route controllers (e.g. system.py)
│   │       ├── dependencies/    # FastAPI dependency injections
│   │       └── router.py        # Central Router for v1
│   │
│   ├── core/
│   │   ├── config.py            # Pydantic Configuration Management
│   │   ├── logger.py            # Standardized logger
│   │   ├── security.py          # Security and auth functions (placeholder)
│   │   └── constants.py         # System constants
│   │
│   ├── database/
│   │   └── connection.py        # Database connection and session lifecycle
│   │
│   ├── services/                # Business logic layer
│   ├── schemas/                 # Pydantic schemas (DTOs)
│   ├── utils/                   # Helper functions
│   │
│   └── main.py                  # Entrypoint of the FastAPI app
│
├── tests/                       # Testing module
├── docs/                        # Static API documentation
├── scripts/                     # Helper script utilities
│
├── requirements.txt             # Project requirements
├── .env                         # Local configuration variables
├── .gitignore                   # Files excluded from git
└── README.md                    # Module documentation
```

## 🛠️ Tech Stack
- **FastAPI**: Modern, high-performance web framework for Python APIs.
- **SQLAlchemy**: Relational database ORM.
- **Psycopg2-binary**: PostgreSQL engine driver.
- **Pydantic / Pydantic-settings**: Data modeling and settings parsing from `.env`.

## 🚀 Execution & Command Reference

### Local Setup
1. Create a virtual environment inside the `traffic-violation-system` directory:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows PowerShell**: `.\venv\Scripts\Activate.ps1`
   - **Linux/macOS**: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Endpoint Reference
- **Root Welcome**: `GET /api/v1/`
- **System Health**: `GET /api/v1/health`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
