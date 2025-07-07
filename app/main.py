from uuid import UUID
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database import Base, engine, get_db
from app.exceptions import AppointmentNotFoundException, DoctorBusyException
from app.schemas import AppointmentCreate, AppointmentResponse
from app.services import AppointmentService


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinic Appointments API",
    description="Microservice for managing doctor appointments",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DoctorBusyException)
async def handle_doctor_busy(request, exc: DoctorBusyException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )


@app.exception_handler(AppointmentNotFoundException)
async def handle_not_found(request, exc: AppointmentNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

@app.post(
    "/appointments",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    service = AppointmentService(db)
    return service.create_appointment(appointment)


@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    service = AppointmentService(db)
    return service.get_appointment(appointment_id)


@app.get("/health")
def health_check():
    return {"status": "ok"}

