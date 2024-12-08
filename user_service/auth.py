import jwt
from datetime import timedelta,datetime
from config import TokenConfig

def generate_token(
	payload:dict,
	private_key:str= TokenConfig.private_key,
	algorithm:str =TokenConfig.algorithm, 
	exp:timedelta= TokenConfig.expire_min			   
) ->str:
	to_encode = payload.copy()
	to_encode['exp'] = datetime.utcnow() + exp 

	token = jwt.encode(to_encode,private_key,algorithm)	
	print(token)
	return token 

