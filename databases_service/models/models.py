from pydantic import BaseModel, Field, AfterValidator
from enum import Enum


class DBModel(BaseModel):  # Model which represent databases table in our main db
    id: str
    db_name: str
    db_system: str
    password: str
    user_id: str  # whose database is this


class DBSystemsEnum(str, Enum):
    postgres = "postgres"
    mongodb = "mongodb"


class DBCreateModel(BaseModel):
    db_name: str
    db_system: DBSystemsEnum
    password: str

