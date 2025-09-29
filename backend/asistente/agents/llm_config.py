import os
from langchain_openai import ChatOpenAI

# instancia del modelo openAI con configuración personalizada
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=300, # Limitar tokens de salida para evitar respuestas demasiado largas
    streaming=True, # Habilitar streaming para respuestas más rápidas
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# llm = ChatOpenAI(
#     model="deepseek-chat",
#     temperature=0.2,
#     max_tokens=300, # Limitar tokens de salida para evitar respuestas demasiado largas
#     streaming=True, # Habilitar streaming para respuestas más rápidas
#     openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
#     openai_api_base=os.getenv("OPENAI_API_BASE")
# )
