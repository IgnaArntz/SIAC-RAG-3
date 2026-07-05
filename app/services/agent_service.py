from app.services.tools_service import (
    search_documents,
    search_memory
)

from app.services.memory_service import (
    save_message
)


def agent_answer(question):

    # Guardar pregunta del usuario
    save_message("user", question)

    lower_question = question.lower()

    # Palabras clave para activar memoria
    memory_keywords = [
        "recuerdas",
        "dije",
        "historial",
        "antes",
        "conversación",
        "pregunté"
    ]

    # DECISIÓN 1:
    # Consultar memoria
    if any(word in lower_question for word in memory_keywords):

        response = search_memory()

    # DECISIÓN 2:
    # Detectar presentación del usuario
    elif "mi nombre es" in lower_question:

        response = (
            "He registrado tu nombre en la memoria temporal."
        )

    # DECISIÓN 3:
    # Consultar base documental (RAG)
    else:

        response = search_documents(question)

    # Guardar respuesta del agente
    save_message("assistant", response)

    return response
