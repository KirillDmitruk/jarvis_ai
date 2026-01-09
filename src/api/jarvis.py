from fastapi import Body, Request, APIRouter
from fastapi.encoders import jsonable_encoder

from src.ai.ai_client import AIClient
from src.db import get_user_requests, add_request_data

router = APIRouter()
ai = AIClient()


@router.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    print(f"{user_ip_address=}")
    user_requests = get_user_requests(ip_address=user_ip_address)
    return jsonable_encoder(user_requests)


@router.post("/requests")
def send_prompt(
        request: Request,
        prompt: str = Body(embed=True),
):
    user_ip_address = request.client.host
    answer = ai.ask(prompt)
    add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        response=answer,
    )
    return {"answer": answer}
