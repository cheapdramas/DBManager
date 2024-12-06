from fastapi import APIRouter,HTTPException
from models.user import UserRegister,User
import psycopg
from config import DatabaseConfig

router = APIRouter()

@router.delete('/user')
async def delete_user_route(user_id:str):
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