import psycopg
from fastapi import APIRouter,HTTPException,status
from models.user import UserRegister,User
from config import DatabaseConfig
from auth import decode_token
from jwt.exceptions import InvalidTokenError
router = APIRouter()

@router.delete('/user')
async def delete_user_route(access_token:str) -> None:
	try:
		payload = decode_token(access_token)
	except InvalidTokenError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Signature error')
	user_id = payload['user_id']
	await RouteHelpersFuncs().delete_user_from_db(user_id)



def RouteHelpersFuncs(): #proxy function for accessing class that i wrote below endpoints just because
	return RouteHelpersFuncs()
class RouteHelpersFuncs():
	@staticmethod
	async def connect_to_db(**kwargs) -> psycopg.connection_async.AsyncConnection:
		conninfo = f"""
			host={DatabaseConfig.host} 
			dbname={DatabaseConfig.database} 
			user={DatabaseConfig.user} 
			password={DatabaseConfig.password} 
		"""
		return await psycopg.AsyncConnection.connect(conninfo,**kwargs)
	@staticmethod
	async def delete_user_from_db(user_id:str):
		sql_query = """
			DELETE FROM users WHERE id=%s
		"""		
		sql_parameters = (user_id,)

		async with await RouteHelpersFuncs.connect_to_db() as conn:
			cursor = conn.cursor()

			await cursor.execute(sql_query,params=sql_parameters)
			await conn.commit()
			
			await cursor.close()