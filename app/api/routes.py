from fastapi import APIRouter

from app.services.agent_service import agent_answer

from app.models.question_model import QuestionRequest
from app.models.response_model import AnswerResponse

from app.monitoring.metrics import get_metrics

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):

    # Validar pregunta vacía
    if not request.question.strip():

        return AnswerResponse(
            response="La pregunta no puede estar vacía."
        )

    response = agent_answer(request.question)

    return AnswerResponse(
        response=response
    )


@router.get("/metrics")
async def metrics():

    return get_metrics()