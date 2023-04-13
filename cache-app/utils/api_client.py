import json
from datetime import timedelta

import httpx
from dependencies import get_redis_conn, get_settings
from fastapi import HTTPException
from utils.exceptions import NoResultFound
from utils.schemas import BookModel, IdModel


def mapping(raw_data: dict) -> dict:

    book = BookModel(
        id=raw_data['id'],
        title=raw_data['title'],
        author=raw_data['author'],
        genre=raw_data['genre'],
        description=raw_data['description'],
        isbn=raw_data['isbn'],
        image=raw_data['image'],
        published=raw_data['published'],
        publisher=raw_data['publisher']
    )

    data = dict(
        id=book.id,
        title=book.title,
        author=book.author,
        genre=book.genre,
        description=book.description,
        isbn=book.isbn,
        image=book.image,
        published=book.published,
        publisher=book.publisher
    )

    return data


def get_data_from_api() -> list | None:
    """Data from api."""
    settings = get_settings()

    with httpx.Client() as client:

        url = settings.api_url
        try:
            response = client.get(url)
            resp = response.json()
            data = [mapping(book) for book in resp["data"]]

            return data

        except HTTPException:
            raise HTTPException(status_code=500, detail='API error request')


def get_data_from_redis(key: str) -> dict:
    """Get data from redis."""

    id = IdModel(id=key).id
    
    book = get_redis_conn().get(id)
    if book:
        book = json.loads(book.decode("utf-8"))
        return book

    return False


def set_data_to_cache(key: str, value: str) -> tuple:
    """Set data to redis."""

    id = IdModel(id=key).id

    state = get_redis_conn().setex(
        id,
        timedelta(seconds=86400),
        value=json.dumps(value),
        )

    try:
        book = get_data_from_redis(id)
        if book:
            return (book, state)
    except Exception:
        NoResultFound()


def get_books(id: str = None):

    if id is not None:
        cache_data = get_data_from_redis(key=id)

        if cache_data:

            return cache_data

        data = get_data_from_api()
        if data:
            book = [book for book in data if id == book['id']]

            if book:

                ingestion = set_data_to_cache(key=id, value=book[0])

                if ingestion:
                    return ingestion[0]
            raise HTTPException(status_code=404, detail="book not found")

    data = get_data_from_api()

    return data
