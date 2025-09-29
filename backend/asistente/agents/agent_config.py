from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor
from .llm_config import llm
from .tools import tools
from .prompt import system_message
from .tokens import count_tokens, count_memory_tokens
from datetime import datetime, timedelta
from .session_manager import clear_session

memory = ConversationBufferMemory(
        memory_key="chat_history", # Clave para almacenar el historial de conversación         
        return_messages=True # Retornar mensajes completos en lugar de solo texto
    )

user_memories = {}
last_activity = {}
total_conversations = 0
current_month = datetime.now().month

def get_or_create_memory(thread_id):
    if thread_id not in user_memories:
        user_memories[thread_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[thread_id]

# Crear el prompt del agente    
prompt = ChatPromptTemplate.from_messages(
    [
        system_message, # Mensaje del sistema con instrucciones
        MessagesPlaceholder(variable_name="chat_history"), # Historial de conversación 
        MessagesPlaceholder(variable_name="agent_scratchpad"), # Pasos intermedios del agente
        HumanMessagePromptTemplate.from_template("{input}") # Mensaje del usuario con la entrada actual
    ]
)
# Crear el agente con Function Calling y herramientas
agent_ia = create_openai_functions_agent(
    llm=llm, # Modelo de lenguaje utilizado
    tools=tools, # Herramientas disponibles para el agente
    prompt=prompt # Plantilla de prompt donfigurado para el agente
)

# Función para responder a mensajes utilizando el agente configurado
def responder_ia_langchain(mensaje, thread_id):        
    global total_conversations, current_month
    print(f"Mes actual: {current_month}")

    tiempo_inactividad = timedelta(minutes=5) # Definir tiempo de inactividad
    now = datetime.now() 

    if now.month != current_month:
        print(f"🔁 Mes anterior: {current_month} Cambiado a mes actual → {now.month}. Reiniciando contador mensual.")
        total_conversations = 0
        current_month = now.month

    ultima_actividad = last_activity.get(thread_id)

    if ultima_actividad:
        if now - ultima_actividad > tiempo_inactividad:
            print(f"🕒 Tiempo de inactividad excedido para el usuario {thread_id}. Reiniciando memoria.")            

            user_memories.pop(thread_id, None)  # Reiniciar memoria si ha pasado el tiempo de inactividad
            last_activity.pop(thread_id, None)  # Reiniciar última actividad   
            clear_session(thread_id) #Reiniciar la sesión global          

    memory = get_or_create_memory(thread_id)        
    if not memory.chat_memory.messages:
        print(f"❗ No hay mensajes en la memoria para el usuario {thread_id}.")
        total_conversations += 1

    last_activity[thread_id] = now  # Actualizar última actividad del hilo

    if total_conversations > 3500:
        print(f"🔄 Límite de conversaciones procesadas: {total_conversations}")
        return "Ha alzanzado el límite de conversaciones procesadas en el mes."
    
    # Inicializar el agente con las herramientas, memoria y gestor de conversación
    agent_executor = AgentExecutor(
        agent=agent_ia, # Agente configurado con las herramientas y prompt
        tools=tools, # Herramientas disponibles para el agente
        memory=memory, # Memoria de conversación para mantener el contexto
        verbose=True, # Habilitar salida detallada para depuración
        max_iterations=5, # Número máximo de iteraciones para el agente
        output_key="output", # Clave de salida para el resultado final del agente
        handle_parsing_errors=True
    )
    # Enviar el mensaje al agente y obtener la respuesta
    respuesta = agent_executor.invoke({"input": mensaje})
    
    print("Conversaciones totales global: ", total_conversations)    

    # Retornar la salida del agente
    # return respuesta["output"]
    output = respuesta["output"]
    if "obteniendo" in output.lower() or "un momento" in output.lower():
        return "Estoy procesando tu solicitud, escribe de nuevo en un minuto por favor... ✅"
    return output


