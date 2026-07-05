import time

from app.services.vector_service import get_retriever

from app.monitoring.metrics import (
    register_request,
    register_success,
    register_error,
    register_latency
)

from app.monitoring.logger import logger


def ask_question(question):

    start_time = time.time()

    register_request()

    try:

        print("Pregunta recibida:", question)

        logger.info(
            f"Pregunta recibida: {question}"
        )

        print("LOGGER FUNCIONANDO")

        retriever = get_retriever()

        docs = retriever.invoke(question)

        if not docs:

            logger.warning(
                "No se encontró información relevante."
            )

            register_error()

            latency = time.time() - start_time
            register_latency(latency)

            return "No se encontró información relevante en los documentos."

        context = "\n\n".join(
            [doc.page_content for doc in docs[:3]]
        )

        register_success()

        latency = time.time() - start_time
        register_latency(latency)

        logger.info(
            "Respuesta generada correctamente."
        )

        logger.info(
            f"Latencia: {round(latency, 2)} segundos"
        )

        return context

    except Exception as e:

        register_error()

        latency = time.time() - start_time
        register_latency(latency)

        logger.error(
            f"Error detectado: {str(e)}"
        )

        print("ERROR GENERAL:", repr(e))

        return f"ERROR REAL: {repr(e)}"