import tiktoken

# Inicializar el encoder de tiktoken para contar tokens
try:
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
except KeyError:
    # Si no reconoce el modelo, usar el encoding estándar
    encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    """Función simple para contar tokens de un texto"""
    return len(encoding.encode(text))

def count_memory_tokens(memory):
    """Función para contar tokens de la memoria de conversación"""
    try:
        # Obtener todos los mensajes de la memoria
        messages = memory.chat_memory.messages
        total_tokens = 0
        
        print(f"   📚 Analizando {len(messages)} mensajes en memoria:")
        
        for i, message in enumerate(messages):
            if hasattr(message, 'content'):
                message_content = str(message.content)
                message_tokens = count_tokens(message_content)
                total_tokens += message_tokens
                
                # Mostrar tipo de mensaje (Human/AI)
                message_type = "👤 Usuario" if hasattr(message, 'type') and message.type == 'human' else "🤖 Asistente"
                message_preview = message_content[:30] + "..." if len(message_content) > 30 else message_content
                print(f"      {i+1}. {message_type}: '{message_preview}' → {message_tokens} tokens")
        
        return total_tokens
    except Exception as e:
        print(f"   ❌ Error contando tokens de memoria: {e}")
        return 0