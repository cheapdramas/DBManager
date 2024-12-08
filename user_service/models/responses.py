from pydantic import BaseModel


class TokenInfo(BaseModel):
	access_token:str
	refresh_token:str = None
class UserInfo(BaseModel):
	login:str
	name:str
	email:str