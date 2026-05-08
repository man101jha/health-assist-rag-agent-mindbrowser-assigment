# HealthAssist AI: Production-Ready Healthcare RAG Assistant
A high-performance, memory-efficient Healthcare AI Assistant built with FastAPI and Angular, optimized for production cloud environments.

**Live Demo**: [health-assist-rag-agent-mindbrowser.onrender.com](https://health-assist-rag-agent-mindbrowser.onrender.com/)

---

## 🧱 System Architecture

```text
                                  +-------------------+
                                  |   User Browser    |
                                  +---------+---------+
                                            |
                                  +---------v---------+
                                  |  Angular Frontend |
                                  +---------+---------+
                                            | (REST API)
                                  +---------v---------+
                                  |  FastAPI Backend  |
                                  +----+----+----+----+
                                       |    |    |
           +---------------------------+    |    +---------------------------+
           |                                |                               |
+----------v----------+          +----------v----------+          +----------v----------+
|      Groq LLM       |          |      FastEmbed      |          |      Mock Tools     |
| (Intent + Answer)   |          |  (ONNX Embeddings)  |          | (Appt. Scheduling)  |
+----------^----------+          +----------+----------+          +----------+----------+
           |                                |                               |
           |                     +----------v----------+                    |
           |                     |  Pinecone Vector DB |                    |
           +---------------------+  (Serverless Index) |                    |
                                 +---------------------+                    |
                                            |                               |
                                            +-------------------------------+
```

---

## 🛠️ Tech Stack & Rationale

| Component | Technology | Honest Rationale |
|-----------|------------|------------------|
| **LLM** | Llama 3-70B (via Groq) | Chosen for sub-second inference speeds (300+ tokens/sec) and superior reasoning compared to smaller 7B/8B models. |
| **Embeddings**| FastEmbed (BGE-Small) | Memory-efficient ONNX runtime; critical for production stability as it avoids the 1GB+ RAM overhead of PyTorch-based models. |
| **Vector DB** | Pinecone | Serverless managed service; eliminates the need to manage local storage and provides high-availability semantic search. |
| **Frontend** | Angular 18 | Selected for its strict typing and robust component architecture, ideal for scalable healthcare dashboards. |
| **Backend** | FastAPI | High-performance asynchronous Python framework with built-in Pydantic validation for structured medical data. |

---

## 🚀 Setup & Installation

### 🐳 Docker Compose (Recommended)
This will run both the backend and frontend in isolated containers.
```bash
docker-compose up --build
```

### 🐍 Local Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 🅰️ Local Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 🧪 API Examples

### 1. Ask a Question (`POST /ask`)
**Payload:**
```json
{
  "query": "How do I book an appointment?",
  "history": []
}
```
**Sample Response:**
```json
{
  "answer": "I can help with that! Which department would you like to visit: Cardiology, General, or Diabetes?",
  "source": [],
  "confidence": "high"
}
```

### 2. Sync Documents (`POST /ingest`)
**Sample Response:**
```json
{
  "status": "success",
  "documents_processed": 9,
  "message": "Pinecone index successfully updated."
}
```

### 3. System Health Check (`GET /health`)
**Sample Response:**
```json
{
  "status": "healthy",
  "app_name": "HealthAssist AI",
  "version": "1.0.0"
}
```

---

## 📝 Sample Q&A Gallery

| Topic | Sample Question | Sample Response | Source File |
|-------|-----------------|-----------------|-------------|
| **Telehealth** | "Can I see a doctor online today?" | "Yes, we offer telehealth consultations for non-emergency issues. You can book a virtual visit through our portal." | `telehealth_consultation_policy.txt` |
| **Medication** | "How do I request a refill for my meds?" | "To request a refill, please contact your pharmacy directly or use our patient portal. Allow 48 hours for processing." | `medication_refill_policy.txt` |
| **Privacy** | "Is my medical data shared with others?" | "Our clinic strictly adheres to HIPAA guidelines. Your information is never shared without your explicit written consent." | `hipaa_privacy_guidelines.txt` |
| **Post-Op** | "What if my surgery site looks red?" | "Minor redness is expected, but if you notice increasing pain or discharge, please contact our post-op team immediately." | `discharge_instructions.txt` |
| **Out-of-Scope**| "Who won the World Cup in 2022?" | "I apologize, but we don't have information on that topic. I am here to help you with clinic procedures and medical recovery." | `N/A (Guardrail)` |

---

## 📄 Dataset & Source Details

| File | Topics Covered | Type |
|------|----------------|------|
| `diabetes_patient_guide.txt` | Symptoms, diet, and long-term care. | MedlinePlus-adapted |
| `discharge_instructions.txt` | Post-operative care and emergency signs. | MedlinePlus-adapted |
| `hypertension_guide.txt` | Blood pressure management and lifestyle. | MedlinePlus-adapted |
| `mental_health_guide.txt` | Coping strategies and crisis resources. | MedlinePlus-adapted |
| `appointment_scheduling_policy.txt` | Cancellation rules and waitlist procedures. | Synthetic (Clinic Policy) |
| `hipaa_privacy_guidelines.txt` | Data handling and legal compliance. | Synthetic (Clinic Policy) |
| `insurance_eligibility_faq.txt` | Medicaid/Medicare coverage and billing. | Synthetic (Clinic Policy) |
| `medication_refill_policy.txt` | Refill request timelines and protocols. | Synthetic (Clinic Policy) |
| `telehealth_consultation_policy.txt` | Virtual visit technical requirements. | Synthetic (Clinic Policy) |

---

## 💉 Prompting Strategy

### The System Prompt
```text
You are the official HealthAssist AI, representing our clinic. Always speak as a professional member of our clinic staff.

CORE RULES:
1. NO AI-SPEAK: Never mention "database", "records", "context", "AI", or "training data".
2. FALLBACK: "I apologize, but we don't have information on that specific topic. We are here to help you with our medical procedures..."
3. SPEAK AS "WE": Use "We" or "Our clinic" when referring to medical information.
4. EMERGENCY FIRST: If distress is detected, start with "🚨 EMERGENCY: Please call 911..."
5. FORMATTING: Use **Bold** for emphasis and ### for headers.
```

### Rationale:
- **Emergency First**: Prioritizes patient safety by surfacing emergency warnings immediately.
- **Natural Phrasing**: Prevents technical jargon from breaking the "Clinic Staff" persona.
- **Persona-Based Voice**: Adopting the "We" collective persona builds trust and legitimacy.
- **Structural Clarity**: Mandatory Markdown ensures instructions are readable and scannable.

---

## 🔄 Agent & Tool Workflow

```text
User Query
│
└── 🧠 Intent Classifier (Groq LLM)
    │
    ├── 🤝 GREETING Intent ──> "Hello! How can I help?"
    │
    ├── 📅 BOOKING Intent ──> Tool: appointment_service ──> Response
    │
    └── 📚 KNOWLEDGE Intent (RAG Pipeline)
        │
        └── 🔍 FastEmbed + Pinecone Vector Search
            │
            ├── ✅ Context Found ──> LLM + Context ──> Markdown Answer
            │
            └── ❌ No Context ──> Guardrail Response
```

---

## ⚠️ Limitations & Future Improvements

### 🛑 Current Limitations
1. **No Session Persistence**: Conversation history is stored in memory. Production would use **Redis**.
2. **Mock Integration**: The appointment booking system is currently a mock tool, not a real EHR integration.
3. **Controlled Substances**: Bot does not handle refill requests for controlled substances per policy.
4. **Lack of Auth**: Current deployment is a single-user system; needs **JWT/OAuth2** for production.

### 🚀 Future Roadmap
- **RAGAS Evaluation**: Implement formal evaluation metrics (Faithfulness, Relevance).
- **Multimodal Support**: Add Vision-LLM support for symptom photo analysis.
- **Hybrid Search**: Combine BM25 keyword search with Pinecone semantic search.
- **Voice Interface**: Implement Web Speech API for elderly patients.
