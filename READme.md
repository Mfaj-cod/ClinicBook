# ClinicBook - Agentic AI-Powered Healthcare Platform (Production-Grade)

A **production-ready, multimodal, AI-powered healthcare platform** that transforms appointment booking into an intelligent, conversational workflow.

**ClinicBook** features a **Context-Aware Agentic AI** capable of **reasoning, speaking, listening, reading, writing, and executing actions** across a real clinic management system.

**Live Deployment:** https://clinicagentbook.onrender.com  
**Docker Image:** https://hub.docker.com/r/honeydoc/clinicbook-repo  
**CI/CD:** GitHub Actions → Docker Hub → Render

---

## Key Features

### Agentic AI Health Assistant (Powered by Gemini)
*A hybrid system combining Agentic Tool Use + Retrieval-Augmented Generation (RAG).*

- ** Voice Interface**: Built-in **Speech-to-Text** lets users speak commands like:
  > "Book an appointment", "Create slots for next Monday", "Who is visiting me tomorrow?"

- ** Hybrid RAG System**:
  - **Dynamic Data**: Reads live data from SQLite (doctors, slots, appointments).
  - **Static Knowledge**: Answers clinic policy questions from `clinic_policies.txt` without DB calls.

- ** Context-Aware Reasoning**:
  - Automatically detects **User Role** (Doctor/Patient)
  - Understands **Relative Dates** like *today, tomorrow, next Monday*

- ** Tool-Calling Agent**:
  - Executes DB tools for:
    - Booking appointments
    - Creating slots
    - Marking appointments completed
    - Searching doctors

![Agentic Workflow Diagram](/assets/Agent.jpg)

---

### Doctor Portal

- **Voice-Controlled Slot Management**
- **Smart Dashboard**
- **Ask Natural Questions**:
  > "Who is visiting me today?"

- **Agentic Automation**:
  - Create slots
  - Close appointments
  - Manage schedules through chat

- **Secure Session Isolation**

---

### Patient Portal

- **Symptom-to-Specialist Mapping**
- **One-Click Booking**
- **Ask AI**:
  > "Which doctor should I visit for chest pain?"

- **Transparent Appointment Status & Policies**

---

## Production Architecture
```bash
GitHub Push
↓
GitHub Actions (CI)
↓
Docker Build & Push
↓
Docker Hub
↓
Render Auto Deploy (CD)
↓
Live Production Service
```
---

## Technology Stack

- **Backend**: Flask (Python)
- **AI Engine**: Google Gemini 2.5 Flash
- **AI Architecture**:
  - Agentic Tool Calling
  - Lightweight RAG (Policy Injection)
  - Role-Based System Prompting
- **Frontend**:
  - Bootstrap 5 + Jinja2
  - Web Speech API (Voice)
- **Database**: SQLite
- **DevOps**:
  - Docker
  - GitHub Actions CI/CD
  - Render Image Deployment

---

## AI Query Router Logic

The agent uses a **Router Architecture**:

1. **Knowledge Query**
   > "Do you accept insurance?"
   - Source: `clinic_policies.txt`
   - Action: RAG Response

2. **Data Query**
   > "Find a cardiologist"
   - Tool: `search_doctor_by_specialization`
   - Action: DB Read

3. **Action Command**
   > "Book the 10 AM slot"
   - Tool: `book_appointment_by_patient`
   - Action: DB Write

---

## Run Locally

### Prerequisites

- Python 3.8+
- Google Gemini API Key

### Installation

```bash
git clone https://github.com/Mfaj-cod/ClinicBook.git
cd ClinicBook
python -m venv clinic
clinic\Scripts\activate   # Windows
source clinic/bin/activate # Mac/Linux
pip install -r requirements.txt

Configure Environment

Create .env:

GEMINI_API_KEY=your_api_key
GEMINI_MODEL_NAME=gemini-2.5-flash
SECRET_KEY=your_secret_key

RUN: python app.py
```

### Run with Docker
```bash
docker pull honeydoc/clinicbook-repo:latest
docker run -p 5000:5000 honeydoc/clinicbook-repo
```

---

### Project Structure
```bash
ClinicBook/
├── app.py
├── Dockerfile
├── requirements.txt
├── src/
│   ├── init_db.py
│   ├── seed.py
│   ├── gem.py
│   ├── prompt.py
│   ├── tools_config.json
│   └── doctors_data.py
├── data/
│   ├── clinicBook.db
│   └── clinic_policies.txt
├── templates/
├── static/
└── README.md
```

### Use Cases

- **For Clinics**:
    - AI receptionist
    - Voice-controlled scheduling
    - Zero-dashboard navigation
    - Automated workflows

- **For Patients**:
    - Natural language booking
    - Smart doctor discovery
    - Instant answers
 

## Roadmap

 Agentic AI with tool calling ✔️

 Voice input ✔️

 RAG knowledge base ✔️

 CI/CD deployment ✔️

 Payment gateway

 Analytics dashboard

 Multi-clinic support

### 📞 Support

Open an issue in GitHub for support.

### Built With Purpose

This project demonstrates real-world Agentic AI, DevOps, MLOps, and production system design.