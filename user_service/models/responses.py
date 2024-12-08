from pydantic import BaseModel


class TokenInfo(BaseModel):
	access_token:str