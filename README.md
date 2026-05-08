# HealthAssist AI: Production-Ready Healthcare RAG Assistant

A high-performance, memory-efficient Healthcare AI Assistant built for the Mindbowser AI Role Assignment. This system implements a robust RAG (Retrieval-Augmented Generation) pipeline to provide accurate medical information and appointment guidance.

**Live Demo**: [health-assist-rag-agent-mindbrowser.onrender.com](https://health-assist-rag-agent-mindbrowser.onrender.com/)

---

## 🏗️ Architecture Overview
The system follows a **Modular Monolith** architecture:
- **Frontend**: Angular 18 with a glassmorphic, responsive UI and custom Markdown rendering.
- **Backend**: FastAPI (Python 3.12) orchestrating the RAG pipeline.
- **Vector Store**: Pinecone (Serverless) for high-speed semantic retrieval.
- **Intelligence**: Groq (Llama 3-70B) for ultra-fast, low-latency reasoning.

---

## 🛠️ Tech Stack Details

### 🧠 LLM Used
**Llama 3-70B (via Groq)**: Chosen for its state-of-the-art reasoning and lightning-fast inference speeds (approx. 300 tokens/sec), ensuring a fluid conversational experience.

### 🔢 Embedding Model
**FastEmbed (BGE-Small)**: We use an ONNX-optimized embedding model. This is a critical production choice that reduced RAM usage from 1.2GB (PyTorch) to just 250MB, making the app viable for low-cost cloud deployment.

### 🗄️ Vector Database
**Pinecone**: A serverless vector database used to store medical document embeddings, allowing for sub-millisecond retrieval of relevant context.

### 💉 Prompting Strategy
We use a **Persona-Based System Prompt** that adopts a "Clinic Staff" persona. It focuses on:
- **Structured Markdown**: Ensuring medical instructions are readable (lists, bolding).
- **No technical jargon**: Removing all mentions of "AI," "context," or "database."
- **Few-Shot Examples**: Guiding the model on how to handle appointment booking queries.

### 🔄 Agent/Tool Workflow
1. **Semantic Search**: Retrieves top-k relevant medical chunks from Pinecone.
2. **Context Augmentation**: Injects retrieved knowledge into the LLM prompt.
3. **Response Guardrails**: A custom logic layer checks for "Out of Scope" responses and automatically suppresses citation metadata to prevent false attribution.

---

## 🚀 Setup & Installation

### 🐳 Docker Setup (Recommended)
```bash
docker build -t health-assist .
docker run -p 8000:8000 --env-file .env health-assist
```

### 🐍 Local Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
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

## 🧪 API Examples (curl)

### 1. Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
-H "Content-Type: application/json" \
-d '{
  "query": "How do I book an appointment?",
  "history": []
}'
```

### 2. Sync Documents (Ingestion)
```bash
curl -X POST http://localhost:8000/ingest
```

---

## 📄 Dataset & Source Details
The system is pre-indexed with medical discharge instructions and clinic protocols based on standardized medical guidelines. It handles:
- Appointment scheduling procedures.
- Post-operative wound care.
- Insurance (Medicaid/Medicare) inquiries.

---

## ⚠️ Limitations & Future Improvements
1. **Limitations**: Current system is text-only and has a 512MB RAM constraint on the free tier.
2. **Future Improvement**: **Hybrid Search** (combining keyword and semantic search) for better accuracy on specific medical codes.
3. **Future Improvement**: **Persistent Memory** using Redis to track patient history across multiple sessions.
