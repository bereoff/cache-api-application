
from pydantic import BaseModel, validator


class IdModel(BaseModel):
    id: str

    @validator('id')
    def number_gt(cls, v):
        if int(v) < 1:
            raise ValueError("Invalid id")
        return v

    @validator('id')
    def is_a_number(cls, v):
        if v.isdigit():
            return v
        raise ValueError("Id is not a number!")

    class Config:
        min_anystr_length = 1
        error_msg_templates = {
            'value_error.any_str.min_length': 'min_length:{limit_value}',
        }


class BookModel(BaseModel):

    id: str
    title: str
    author: str
    genre: str
    description: str
    isbn: str
    image: str
    published: str
    publisher: str

    @validator('id')
    def number_gt(cls, v):
        if int(v) < 1:
            raise ValueError("Invalid id")
        return v

    class Config:
        orm_mode = True
        min_anystr_length = 1
        error_msg_templates = {
            'value_error.any_str.min_length': 'min_length:{limit_value}',
        }
