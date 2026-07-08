# AI-Based Smart Traffic Violation Detection System

This repository hosts a production-ready, full-stack real-time computer vision system that monitors video streams, identifies vehicle tracks, and runs AI classifiers to log traffic violations (such as helmet requirements, seat belts, traffic lights, and phone usage).

---

## 📂 Folder Structure

```text
traffic-violation-system/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/          # Routers (camera, violations, evidence, analytics)
│   │       └── router.py        # Central Router registration
│   ├── database/
│   │   ├── models/              # SQLAlchemy Models (Camera, Violation, Evidence)
│   │   └── connection.py        # Lifecycle DB Session managers
│   ├── services/
│   │   ├── camera/              # RTSP / Web stream handlers
│   │   ├── detection/           # YOLO class estimators
│   │   ├── tracking/            # ByteTrack vehicle matching
│   │   ├── violation/           # Rule evaluator engine
│   │   ├── evidence/            # Frame snapshot & video clip recorder
│   │   └── analytics/           # Metric SQL aggregations
│   └── main.py                  # Entrypoint mounting static resources and CORS
│
├── frontend/                    # Vite + React SPA dashboard client
│   ├── src/
│   │   ├── components/          # Navbar, Sidebar, LiveFeed stream canvas, Charts
│   │   ├── pages/               # Dashboard, Violations logs, Evidence Vault, Analytics
│   │   └── services/            # Axios API wrappers
│   └── vite.config.js           # Proxy forwarding configurations
│
├── deployment/                  # Docker container configs
│   ├── docker/
│   │   ├── backend.Dockerfile   # Python compilation environment
│   │   └── frontend.Dockerfile  # Multi-stage SPA bundler
│   ├── nginx/
│   │   └── nginx.conf           # Port 80 ingress configuration
│   └── docker-compose.yml       # Stack coordinator (db, backend, frontend, nginx)
│
├── tests/                       # Unit and Integration test scripts
│   ├── api_tests/               # Endpoint client tests
│   ├── model_tests/             # YOLO load test checks
│   └── integration_tests/       # Pipeline simulation checks
│
├── requirements.txt             # Backend python packages list
└── README.md                    # System documentation guide
```

---

## 🚀 Running Instructions

### 1. Docker Production Compose (Recommended)
Build and spin up the complete containerized full stack:
```bash
cd traffic-violation-system/deployment
docker-compose up -d --build
```
Access points:
* **Frontend Dashboard client**: `http://localhost`
* **Interactive API Swagger Docs**: `http://localhost/docs`

---

### 2. Local Development Execution

#### A. Backend Setup
1. Activate virtual environment:
   `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Unix)
2. Run backend dev server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

#### B. Frontend Setup
1. Install packages:
   ```bash
   cd frontend
   npm install
   ```
2. Start Vite client:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in browser.

---

## 🛠️ Testing reference
Execute all discoverable unit tests from the backend project root folder:
```bash
$env:PYTHONPATH="."
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📧 Email Alerts Setup
Refer to [email_setup.md](file:///c:/Users/Jaspreet/OneDrive/Desktop/Traffic%20violation%20Project/traffic-violation-system/docs/email_setup.md) for full instructions on configuring automated email alerts using SMTP and Google App Passwords.

