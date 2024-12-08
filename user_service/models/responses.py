from pydantic import BaseModel


class TokenInfo(BaseModel):
	access_token:str

class UserInfo(BaseModel):
	login:str
	name:str
	email:str