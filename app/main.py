from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID


from app.database import engine, get_db, Base
from app.schemas import AppointmentCreate, AppointmentResponse
from app.services import AppointmentService
from app.exceptions import DoctorBusyException, AppointmentNotFoundException

Base.metadata.create_all(bind=engine)
print("Все таблицы созданы")

app = FastAPI(
    title="Clinic Appointments API",
    description="Microservice for managing doctor appointments",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    service = AppointmentService(db)
    try:
        return service.create_appointment(appointment)
    except DoctorBusyException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Doctor {e.doctor_id} is already busy at {e.start_time}"
        )

@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db)
):
    service = AppointmentService(db)
    try:
        return service.get_appointment(appointment_id)
    except AppointmentNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {e.appointment_id} not found"
        )

@app.get("/health")
def health_check():
    return {"status": "ok"}

# def main():
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
#
# if __name__ == "__main__":
#     main()