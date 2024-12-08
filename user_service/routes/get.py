import psycopg
from fastapi import APIRouter,HTTPException,status
from psycopg.rows import dict_row
from psycopg.connection_async import AsyncConnection
from config import DatabaseConfig
from models.user import User
from models.responses import UserInfo



router = APIRouter()




@router.get('/users')
async def getting_users_route() -> list[User] | list:
	all_users: list[User|None] = await RouteHelpersFuncs().get_all_users()
	return all_users 

@router.get('/user',response_model=UserInfo)
async def get_user_info_route(user_id:str):
	
	user_info:dict|None = await RouteHelpersFuncs().get_user_info(user_id)
	if user_info == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
	return UserInfo(**user_info)




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
		async with await RouteHelpersFuncs.connect_to_db(row_factory=dict_row) as conn:
			cursor = conn.cursor()

			await cursor.execute('SELECT id,login,name,email FROM users')
			result = await cursor.fetchall()
			await cursor.close()
			await conn.close()
			return result
		
	@staticmethod
	async def get_user_info(user_id:str) -> dict | None:
		async with await RouteHelpersFuncs.connect_to_db(row_factory=dict_row) as conn:
			cursor = conn.cursor()

			await cursor.execute(
				"""	SELECT 
						* 
					FROM users WHERE id=%s
				""",
				params=(user_id,)
			)
			result = await cursor.fetchone()
			await cursor.close()
			await conn.close()
			return result
	
	