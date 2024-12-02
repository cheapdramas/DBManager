from fastapi import HTTPException,status
from pydantic import BaseModel,EmailStr,Field,AfterValidator
from typing import Annotated
import uuid
import re
import bcrypt
class ModelHelpers:

	@staticmethod
	def generate_random_uuid():
		return str(uuid.uuid4())
	@staticmethod
	def validate_name(name:str):
		assert len(name) <= 60
		pattern = r'^[А-ЯA-Z][а-яa-z]+\s[А-ЯA-Z][а-яa-z]+$'
		if not re.match(pattern,name):
			raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail='Failed name validation')
		return name
	def hash_password(password:str) -> bytes:
		return bcrypt.hashpw(password.encode(),bcrypt.gensalt())



class User(BaseModel):
	id:str = Field(default_factory=ModelHelpers.generate_random_uuid)
	login:str
	password:Annotated[bytes,AfterValidator(ModelHelpers.hash_password)]
	name:str #Pidoras Pidorasovich
	email:EmailStr|None


class UserRegister(BaseModel):
	login:str = Field(max_length=50)
	password:str
	name:Annotated[str,AfterValidator(ModelHelpers.validate_name)] = 'David David' #Pidoras Pidorasovich
	email:EmailStr = None


class UserLogin(BaseModel):
	login:str
	password:str