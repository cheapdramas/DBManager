from pydantic import BaseModel
from datetime import timedelta,datetime
from config import TokenConfig

class AccessTokenPayload(BaseModel):
	user_id:str 
	name:str
	email:str

