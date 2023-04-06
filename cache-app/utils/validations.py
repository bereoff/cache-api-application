
from pydantic import BaseModel, validator


class IdModel(BaseModel):
    id: str

    @validator('id')
    def number_gt(cls, v):
        if int(v) < 1:
            raise ValueError("Invalid id")
        return v

    class Config:
        min_anystr_length = 1
        error_msg_templates = {
            'value_error.any_str.min_length': 'min_length:{limit_value}',
        }


class NameModel(BaseModel):
    name: str

    class Config:
        min_anystr_length = 1
        max_anystr_length = 20
        error_msg_templates = {
            'value_error.any_str.min_length': 'min_length:{limit_value}',
            'value_error.any_str.max_length': 'max_length:{limit_value}',
        }


class UserModel(BaseModel):
    id: str
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    ip: str
    macAddress: str
    website: str
    image: str

    @validator('id')
    def number_gt(cls, v):
        if int(v) < 1:
            raise ValueError("Invalid id")
        return v

    @validator('firstname', "lastname")
    def name_length(cls, v):
        data_length = len(v)
        if data_length < 1 or data_length > 20:
            raise ValueError(f"value_error.any_str.min_length: 'min_length:{1}','max_length:{20}'") # noqaE501
        return v

    class Config:
        orm_mode = True
