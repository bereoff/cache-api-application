# from typing import List
import json

from dependencies import get_redis_conn, get_settings
from fastapi import APIRouter, Depends, HTTPException, Response
from utils import api_client
from utils.schemas import BookModel, IdModel

router = APIRouter()


@router.get(
    "/books/validate-db/",
    dependencies=[Depends(get_settings), Depends(get_redis_conn),])
async def check_data_in_redis() -> list[dict]:
    """Checks if is there data at cache."""
    cache_data = get_redis_conn().scan(cursor=0, count=1)

    if cache_data[1]:

        return [{"status": 200}]

    data_ingestion = api_client.get_data_from_api()

    if data_ingestion is not None:

        for book in data_ingestion:
            id = IdModel(id=book['id']).id

            api_client.set_data_to_cache(id, book)

        return [{"ingestion": {"status": 201}}]


@router.get(
    "/book/{id}/",
    dependencies=[Depends(get_settings), Depends(get_redis_conn),],
    status_code=200, response_model=None)
async def get_book_by_id(id: str) -> Response | dict:
    """Get book by id"""
    if id.isdigit():
        id = IdModel(id=id).id

        book = api_client.get_books(id)

        if not book:
            raise HTTPException(status_code=404, detail="book not found")

        return book

    return {"msg": f"The id '{id}' is not a number.", "status code": 400}


@router.get("/books/",
            dependencies=[Depends(get_redis_conn),],
            status_code=200, response_model=None)
async def get_book_by_genre(genre: str) -> Response | list[dict[BookModel]]:
    """Get book by genre"""

    data = get_redis_conn().keys()

    if data:
        results: list = []
        for key in data:
            key = key.decode("utf-8")
            book = get_redis_conn().get(key)
            book = json.loads(book.decode("utf-8"))
            if book['genre'].strip().lower() == genre.strip().lower():
                results.append(book)

        return results

    raise HTTPException(status_code=404, detail="Genre not found")


@router.get("/data-from-api/", dependencies=[Depends(get_settings),])
async def get_data() -> list[dict]:

    return api_client.get_data_from_api()
