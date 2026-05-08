from datetime import datetime, timedelta
import random
from app.core.logger import logger

class AppointmentService:
    def __init__(self):
        # Mock database of doctors and their specialties
        self.doctors = {
            "cardiology": ["Dr. Smith", "Dr. Johnson"],
            "general": ["Dr. Williams", "Dr. Brown"],
            "diabetes": ["Dr. Davis", "Dr. Miller"]
        }

    def check_availability(self, specialty: str):
        """Simulates checking for available slots."""
        specialty = specialty.lower()
        if specialty not in self.doctors:
            return "We don't have that specialty available. We offer Cardiology, General, and Diabetes care."
        
        doctor = random.choice(self.doctors[specialty])
        tomorrow = datetime.now() + timedelta(days=1)
        time_slots = ["09:00 AM", "11:30 AM", "02:00 PM", "04:30 PM"]
        slot = random.choice(time_slots)
        
        return f"{doctor} has an opening tomorrow at {slot}."

    def book_appointment(self, doctor_name: str, date_time: str):
        """Simulates booking the slot."""
        logger.info(f"BOOKING CONFIRMED: {doctor_name} at {date_time}")
        return f"Confirmed! Your appointment with {doctor_name} is scheduled for {date_time}."

appointment_service = AppointmentService()
