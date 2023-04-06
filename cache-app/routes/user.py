# from typing import List
import json

from db import Redis
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
# from pydantic import ValidationError
from utils import function  # get_users_from_api, set_user_to_cache
from utils.validations import IdModel, NameModel, UserModel

router = APIRouter()

conn = Redis.connect()


@router.get("/users/validate-db/")
async def check_data_in_redis() -> list[dict]:
    """List all users."""
    cache_data = conn.scan(cursor=0, count=1)

    if cache_data[1]:

        return [{"status": 200}]

    user_ingestion = function.get_users_from_api()

    if user_ingestion is not None:

        for user in user_ingestion:
            id = IdModel(id=user['id']).id

            function.set_user_to_cache(id, user)

        return [{"ingestion": {"status": 201}}]


@router.get("/user/{id}/", status_code=200, response_model=UserModel)
async def get_user_by_id(id: str) -> str:
    """Get user by username"""

    id = IdModel(id=id).id

    user = function.get_users(id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# TODO: Criar view para filtar por primeiro nome
@router.get("/user/firstname/{name}/",
            status_code=200, response_model=UserModel)
async def get_user_by_firstname(name: str):
    """Get user by firstname"""
    name = NameModel(name=name).name

    data = conn.keys()

    for key in data:
        key = key.decode("utf-8")
        user = conn.get(key)
        user = json.loads(user.decode("utf-8"))
        if user['firstname'] == name:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@router.get("/user-from-api/")
async def get_user_api() -> list[dict]:

    return function.get_users_from_api()
