# ai_care/core/chat_memory.py

# In-memory chat history per user session
# (later we can move to DB)

user_chat_memory = {}

def get_chat_history(user_id: str):
    return user_chat_memory.get(user_id, [])

def add_message(user_id: str, role: str, message: str):
    if user_id not in user_chat_memory:
        user_chat_memory[user_id] = []

    user_chat_memory[user_id].append({
        "role": role,
        "content": message
    })

def clear_chat(user_id: str):
    user_chat_memory[user_id] = []
