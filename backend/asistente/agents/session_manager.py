
USER_SESSIONS = {}

def set_session(user_id, agent_name=None):
    USER_SESSIONS[user_id] = {
        "agent" : agent_name
    }
    print(f"✅ Sesión iniciada para {user_id} con {agent_name}")

def get_session(user_id):
    return USER_SESSIONS.get(user_id)

def clear_session(user_id):
    if user_id in USER_SESSIONS:
        del USER_SESSIONS[user_id]
        print(f"🧹 Sesión eliminada para el usuario {user_id}")

def get_all_sessions():
    return USER_SESSIONS
