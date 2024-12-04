from fastapi import APIRouter,HTTPException
from models.user import UserRegister,User
import psycopg
from config import DatabaseConfig


router = APIRouter()


@router.post('/register')
async def register_user_route(user_info:UserRegister):
	try:
		await RouteHelpersFuncs().add_user(user_info)

		return user_info
	except Exception as e:
		raise HTTPException(400,detail=str(e))
		





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
		connection = await psycopg.AsyncConnection.connect(conninfo=conninfo,**kwargs)
		return connection
	@staticmethod
	async def add_user(user_info:UserRegister):
		new_user = User(**user_info.model_dump())
		sql_query = """
			INSERT INTO users(id,login,password,name,email)
			VALUES (%s,%s,%s,%s,%s)
		"""
		sql_parameters = (
			new_user.id,
			new_user.login,
			new_user.password,
			new_user.name,
			new_user.email
		)

		async with await RouteHelpersFuncs.connect_to_db() as conn:
			cursor = conn.cursor()

			await cursor.execute(sql_query,params=sql_parameters)
			await conn.commit()

			await cursor.close()
			await conn.close()





