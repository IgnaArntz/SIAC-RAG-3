from app.services.memory_service import get_memory
from app.services.rag_service import ask_question


def search_documents(question):

    return ask_question(question)


def search_memory():

    memory = get_memory()

    if not memory:
        return "No existe historial."

    user_messages = [
        m["content"]
        for m in memory
        if m["role"] == "user"
    ]

    if len(user_messages) < 2:
        return "No encuentro mensajes anteriores."

    return f"Antes dijiste: {user_messages[-2]}"