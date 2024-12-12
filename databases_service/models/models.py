from pydantic import BaseModel,Field,AfterValidator
from uuid import uuid4
from typing import Annotated
import json
from enum import Enum


class DBModel(BaseModel): #Model which represent databases table in our main db
	id:str
	db_name:str
	db_system:str
	password:str
	user_id:str #whose database is this


class DBSystemsEnum(str,Enum):
	postgres='postgres'
	mongodb='mongodb'


class DBRegistration(BaseModel):
	db_name:str
	db_system:DBSystemsEnum
	password:str
	user_id:str

