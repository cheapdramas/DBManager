import psycopg
import bcrypt
from fastapi import APIRouter,HTTPException
from models.user import UserRegister,User,UserLogin
from config import DatabaseConfig


router = APIRouter()


@router.post('/register')
async def register_user_route(user_info:UserRegister):
	try:
		await RouteHelpersFuncs().add_user(user_info)

		return user_info
	except Exception as e:
		raise HTTPException(400,detail=str(e))
		
@router.post('/login')
async def login_user_route(login_info:UserLogin):
	pass





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
	#NOT FINISHED
	@staticmethod
	async def login_user(login_info:UserLogin):
		async with await RouteHelpersFuncs().connect_to_db() as conn:
			sql_query_pw = """
				SELECT password FROM users WHERE login=%s
			"""
			cursor = conn.cursor()
			await cursor.execute(sql_query_pw,params=(login_info.login))
			pw_from_db=await cursor.fetchone()
			pw_from_db:bytes =pw_from_db[0]
			if pw_from_db == None:
				raise HTTPException(status_code=404,detail='User not found')
			if not bcrypt.checkpw(login_info.password.encode(),pw_from_db):
				raise HTTPException(status_code=404,detail='User not found(wrong password)')

			


			await cursor.close
			await conn.close
		




