from fastapi import APIRouter
import psycopg
from psycopg.rows import dict_row
from psycopg.connection_async import AsyncConnection
from config import DatabaseConfig




router = APIRouter()




@router.get('/users')
async def getting_users_route():
	return str((await RouteHelpersFuncs().get_all_users(),await RouteHelpersFuncs.connect_to_db()))

@router.get('/user')
async def get_user_info_route(user_id:str):

	return await RouteHelpersFuncs().get_user_info(user_id)





def RouteHelpersFuncs(): #proxy function for accessing class that i wrote below endpoints just because
	return RouteHelpersFuncs()
class RouteHelpersFuncs():
	@staticmethod
	async def connect_to_db(**kwargs) -> AsyncConnection:
		conninfo = f"""
			host={DatabaseConfig.host} 
			dbname={DatabaseConfig.database} 
			user={DatabaseConfig.user} 
			password={DatabaseConfig.password} 
		"""
		connection = await psycopg.AsyncConnection.connect(conninfo=conninfo,**kwargs)
		return connection

	@staticmethod
	async def get_all_users():
		async with await RouteHelpersFuncs.connect_to_db() as conn:
			cursor = conn.cursor()

			await cursor.execute('SELECT * FROM users')
			result = await cursor.fetchall()
			await cursor.close()
			return result
		
	@staticmethod
	async def get_user_info(user_id:str):
		async with await RouteHelpersFuncs.connect_to_db(row_factory=dict_row) as conn:
			cursor = conn.cursor()

			await cursor.execute(
				"""	SELECT 
						login,
						name,
						email 
					FROM users WHERE id=%s
				""",
				params=(user_id,)
			)
			result = await cursor.fetchone()
			await cursor.close()
			return result
	