import requests, pytz, os
from datetime import datetime, timedelta
from langchain.tools import StructuredTool
from .schemas import AppointmentDataInput, HoursInput
from asistente.agents.llm_config import llm
from langchain_core.prompts import PromptTemplate
import random

api_server = os.getenv("URL_SERVER")

def get_current_date():
    try:
        zona_horaria = pytz.timezone('Etc/GMT+5')
        fecha_actual = datetime.now(zona_horaria)

        return {
            "current_date": fecha_actual.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z",
            "day_of_week": fecha_actual.strftime('%A')       
        }
    except Exception as e:
        print(f"Error al obtener la fecha actual: {e}")
        return None


# Definir la herramienta para obtener ciudades
tools = [
    StructuredTool.from_function(
        name="get_current_date",
        func=get_current_date,
        description="Obtiene la fecha y hora actual en formato UTC."
    )
]