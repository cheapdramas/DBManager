from fastapi import HTTPException,status
from pydantic import BaseModel,EmailStr,Field,AfterValidator,model_validator
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
	password:Annotated[str,AfterValidator(ModelHelpers.hash_password)]
	name:str 
	email:EmailStr|None


class UserRegister(BaseModel):
	login:str = Field(max_length=50)
	password:str
	name:Annotated[str,AfterValidator(ModelHelpers.validate_name)] = 'David David'
	email:EmailStr = None


class UserLogin(BaseModel):
	login:str
	password:str

class UserUpdate(BaseModel):
	login:str = None
	name: str = None
	email:str = None
	@model_validator(mode='after')
	def at_least_one_update_value(cls,v):
		
		

		if v.login == None and v.name==None and v.email==None:
			raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail='At least one update value is required')
		update_dict = {}#dict without none values for update
		bad_dict_model = v.model_dump()
		for i in bad_dict_model:
			if bad_dict_model[i] !=None:
				update_dict[i]=bad_dict_model[i]

		return update_dict
	password_confirm:str

	