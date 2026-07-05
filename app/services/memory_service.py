chat_memory = []


def save_message(role, content):

    chat_memory.append({
        "role": role,
        "content": content
    })

    # Mantener últimos 20 mensajes
    if len(chat_memory) > 20:
        chat_memory.pop(0)


def get_memory():

    return chat_memory
