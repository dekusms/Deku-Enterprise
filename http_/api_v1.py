"""API V1 Routes"""

from fastapi import APIRouter, HTTPException
from http_.schemas import (
    UserCreateRequestV1,
    ExchangeCreateRequestV1,
    ErrorResponse,
    UserCreateResponseV1,
    ExchangeCreateResponseV1,
)

from rmq import Exchange

router = APIRouter(prefix="/v1", tags=["API V1"])


@router.post(
    "/users",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=UserCreateResponseV1,
)
def create_user(user: UserCreateRequestV1) -> UserCreateResponseV1:
    return {"message": "User created successfully", "username": user.username}


@router.post(
    "/exchanges",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=ExchangeCreateResponseV1,
)
def create_exchange(exchange: ExchangeCreateRequestV1) -> ExchangeCreateResponseV1:
    exchange_instance = Exchange(vhost=exchange.vhost)
    result, error = exchange_instance.create(
        name=exchange.name,
        type=exchange.type,
        vhost=exchange.vhost,
        durable=exchange.durable,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Exchange created successfully", "result": result}
