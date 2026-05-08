import requests
import json
import time
import os

API_URL = "http://127.0.0.1:8001/ask/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "../../data/test_questions.txt"))
REPORT_FILE = os.path.join(SCRIPT_DIR, "rag_test_report.md")
print(f"DEBUG: Looking for questions at: {QUESTIONS_FILE}")

def parse_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # Look for lines starting with a number and a dot (e.g. "1. What is...")
            if line and line[0].isdigit() and ". " in line:
                q_text = line.split(". ", 1)[1]
                questions.append(q_text)
    return questions

def run_tests():
    questions = parse_questions(QUESTIONS_FILE)
    print(f"Loaded {len(questions)} questions. Starting tests...")
    
    results = []
    
    for i, q in enumerate(questions):
        print(f"[{i+1}/{len(questions)}] Testing: {q[:50]}...")
        start_time = time.time()
        
        try:
            response = requests.post(API_URL, json={"query": q, "history": []})
            duration = round(time.time() - start_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "id": i+1,
                    "question": q,
                    "answer": data["answer"],
                    "confidence": data["confidence"],
                    "latency": duration,
                    "status": "PASS ✅"
                })
            else:
                results.append({"id": i+1, "question": q, "status": f"FAIL ❌ (HTTP {response.status_code})"})
        except Exception as e:
            results.append({"id": i+1, "question": q, "status": f"ERROR ⚠️ ({str(e)})"})

    generate_report(results)

def generate_report(results):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# RAG System Evaluation Report\n\n")
        f.write(f"Generated on: {time.ctime()}\n\n")
        f.write("| ID | Question | Status | Confidence | Latency (s) | Answer |\n")
        f.write("|----|----------|--------|------------|-------------|--------|\n")
        
        for r in results:
            ans = r.get("answer", "N/A").replace("\n", " ")[:100] + "..."
            f.write(f"| {r['id']} | {r['question']} | {r['status']} | {r.get('confidence', 'N/A')} | {r.get('latency', 'N/A')} | {ans} |\n")
    
    print(f"Done! Report generated at: {REPORT_FILE}")

if __name__ == "__main__":
    run_tests()
