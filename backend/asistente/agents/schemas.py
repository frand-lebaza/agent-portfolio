from pydantic import BaseModel


class HoursInput(BaseModel):
    date: str

class AppointmentDataInput(BaseModel):
    nombre: str
    apellido: str    
    telefono: str    
    fecha_cita: str
    hora_cita: str

