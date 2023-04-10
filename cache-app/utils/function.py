import json
from datetime import timedelta

import httpx
from config import settings
from db import Redis
from fastapi.exceptions import HTTPException
from utils.exceptions import NoResultFound
from utils.validations import IdModel, UserModel

conn = Redis.connect()


def mapping(raw_data: dict) -> dict:

    # id = IdModel(id=raw_data['id']).id

    user = UserModel(
        id=raw_data['id'],
        firstname=raw_data['firstname'],
        lastname=raw_data['lastname'],
        username=raw_data['username'],
        password=raw_data['password'],
        email=raw_data['email'],
        ip=raw_data['ip'],
        macAddress=raw_data['macAddress'],
        website=raw_data['website'],
        image=raw_data['image']

    )

    data = dict(
        id=user.id,
        firstname=user.firstname.lower(),
        lastname=user.lastname.lower(),
        username=user.username,
        password=user.password,
        email=user.email,
        ip=user.ip,
        macAddress=user.macAddress,
        website=user.website,
        image=user.image
    )

    return data


def get_users_from_api() -> list | None:
    """Data from mapbox api."""

    with httpx.Client() as client:

        url = settings.API_URL
        try:
            response = client.get(url)
            resp = response.json()
            data = [mapping(user) for user in resp["data"]]

            return data

        except HTTPException:
            raise HTTPException(status_code=500, detail='API error request')


def get_user_from_cache(key: str) -> dict:
    """Get data from redis."""

    id = IdModel(id=key).id

    user = conn.get(id)
    if user:
        user = json.loads(user.decode("utf-8"))
        return user

    return False


def set_user_to_cache(key: str, value: str) -> tuple:
    """Set data to redis."""

    id = IdModel(id=key).id

    state = conn.setex(
        id,
        timedelta(seconds=86400),
        value=json.dumps(value),
        )

    try:
        user = get_user_from_cache(id)
        if user:
            return (user, state)
    except Exception:
        NoResultFound()


def get_users(id: str = None):

    if id is not None:
        cache_data = get_user_from_cache(key=id)

        if cache_data:

            return cache_data

        data = get_users_from_api()
        if data:
            user = [user for user in data if id == user['id']]

            if user:

                ingestion = set_user_to_cache(key=id, value=user[0])

                if ingestion:
                    return ingestion[0]
            raise HTTPException(status_code=404, detail="User not found")

    data = get_users_from_api()

    return data
