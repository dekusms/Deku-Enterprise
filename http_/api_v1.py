"""API V1 Routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from http_.schemas import v1
from services.users import UserService
from db import get_db
from rmq import Exchange

router = APIRouter(prefix="/v1", tags=["API V1"])


@router.post("/users", response_model=v1.UserResponse)
def create_user(user: v1.UserCreateRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    created_user = user_service.create_user(
        username=user.username, password=user.password
    )
    return created_user


@router.get("/users/{user_id}", response_model=v1.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=v1.UserResponse)
def update_user(
    user_id: int, user: v1.UserUpdateRequest, db: Session = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = user_service.update_user(
        user_id, username=user.username, password=user.password
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.post(
    "/exchanges",
    responses={
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
    response_model=v1.ExchangeCreateResponse,
)
def create_exchange(exchange: v1.ExchangeCreateRequest) -> v1.ExchangeCreateResponse:
    exchange_instance = Exchange(vhost=exchange.vhost)
    result, error = exchange_instance.create(
        name=exchange.name,
        type=exchange.type,
        vhost=exchange.vhost,
        durable=exchange.durable,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {
        "name": exchange.name,
        "type": exchange.type,
        "vhost": exchange.vhost,
        "durable": exchange.durable,
        "created_at": "2023-01-01T00:00:00Z",  # Example timestamp
    }
