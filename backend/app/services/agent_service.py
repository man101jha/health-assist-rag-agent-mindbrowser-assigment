import json # Add this import at the top
from groq import Groq
from app.core.config import get_settings
from app.services.rag_service import rag_service
from app.services.appointment_service import appointment_service
from app.core.logger import logger

settings = get_settings()

class AgentService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    async def route_request(self, query: str, history: list = None):
        """Classifies intent and checks for required appointment 'slots'."""
        
        history_text = ""
        if history:
            for msg in history:
                history_text += f"{msg['role'].upper()}: {msg['content']}\n"
        
        # 1. Intent & Entity Extraction Prompt
        extraction_prompt = f"""
        ROLE: You are a Strict Entity Extractor for a Healthcare Clinic.
        
        TASK:
        Extract the Intent, Department, Date, and Confirmation Status.
        
        CHAT HISTORY:
        {history_text}
        
        CURRENT USER QUERY: 
        {query}
        
        STRICT RULES:
        1. DO NOT GUESS. If the user doesn't name a department, return null.
        2. 'is_confirmation' is TRUE if the user says 'Yes', 'Confirm', 'That works', or 'Book it' in response to an available slot mentioned in the history.
        3. Intent is 'BOOKING' if they want to see a doctor or are in the process of confirming a slot.
        4. Intent is 'GREETING' if the user is saying hello, hi, asking 'who are you', or making general small talk.
        5. Intent is 'BOOKING' if they want to see a doctor or confirm a slot.
        6. Intent is 'KNOWLEDGE' if they are asking a health-related question
        
        Return ONLY a JSON object:
        {{
          "intent": "GREETING" | "BOOKING" | "KNOWLEDGE",
          "department": "Cardiology" | "General" | "Diabetes" | null,
          "date": "string or null",
          "is_confirmation": boolean
        }}
        """
        
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            response_format={ "type": "json_object" },
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0
        )
        
        data = json.loads(response.choices[0].message.content)
        intent = data.get("intent", "KNOWLEDGE")
        dept = data.get("department")
        date = data.get("date")
        is_confirm = data.get("is_confirmation", False)

        logger.info(f"Agent Logic -> Intent: {intent}, Dept: {dept}, Date: {date}, Confirm: {is_confirm}")

        if intent == "GREETING":
            return {
                "answer": "Hello! I'm your HealthAssist AI. I can help you find medical information from our documents or schedule an appointment with one of our doctors. How can I help you today?",
                "sources": [],
                "confidence": "high"
            }

        # 2. Routing Logic
        if intent == "BOOKING":
            # HANDLE CONFIRMATION
            if is_confirm:
                final_dept = dept if dept else "general"
                booking_msg = appointment_service.book_appointment(final_dept, "tomorrow")
                return {
                    "answer": booking_msg,
                    "sources": [],
                    "confidence": "high"
                }

            # HANDLE MISSING INFO
            if not dept and not date:
                return {
                    "answer": "I'd be happy to help you book an appointment! Which department would you like to visit (Cardiology, General, or Diabetes)?",
                    "sources": [],
                    "confidence": "high"
                }
            elif not dept:
                return {
                    "answer": f"I can look for an opening. Which department do you need: Cardiology, General, or Diabetes?",
                    "sources": [],
                    "confidence": "high"
                }
            else:
                # FIND AVAILABILITY
                availability = appointment_service.check_availability(dept)
                return {
                    "answer": f"I found an opening for your {dept} request! {availability} Should I confirm this for you?",
                    "sources": [],
                    "confidence": "high"
                }
        
        # Default to RAG for KNOWLEDGE intent
        return await rag_service.answer_question(query)

agent_service = AgentService()
