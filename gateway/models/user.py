from pydantic import BaseModel,EmailStr


class User(BaseModel):
	id:str
	login:str
	password:str
	name:str
	email:EmailStr


class UserRegister(BaseModel):
	login:str
	password:str
	name:str = 'David David'
	email:EmailStr


class UserLogin(BaseModel):
	login:str
	password:str

class UserUpdate(BaseModel):
	login:str = None
	name: str = None
	email:str = None
	password_confirm:str