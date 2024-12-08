import bcrypt
import psycopg
from fastapi import APIRouter,HTTPException
from psycopg.rows import dict_row
from models.user import UserRegister,User,UserLogin
from models.tokens import AccessTokenPayload
from models.responses import TokenInfo
from config import DatabaseConfig,TokenConfig
from auth import generate_token

router = APIRouter()


@router.post('/register')
async def register_user_route(user_info:UserRegister):
	try:
		await RouteHelpersFuncs().add_user(user_info)

		return user_info
	except Exception as e:
		raise HTTPException(400,detail=str(e))
		
@router.post('/login',response_model=TokenInfo)
async def login_user_route(login_info:UserLogin):
	
	access_token = await RouteHelpersFuncs().login_user(login_info)
	return TokenInfo(access_token=access_token)




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
	async def login_user(login_info:UserLogin) ->str:
		async with await RouteHelpersFuncs().connect_to_db(row_factory=dict_row) as conn:
			sql_query = """
				SELECT * FROM users WHERE login = %s
			"""			
			sql_parameters = (login_info.login,)
			cursor = conn.cursor()

			await cursor.execute(
				query=sql_query,
				params=sql_parameters
			)
			user_info_fetch:dict = await cursor.fetchone()
			if user_info_fetch == None:
				raise HTTPException(status_code=404,detail='User not found(null result)')
			pw_from_db:bytes = user_info_fetch['password']

			if not bcrypt.checkpw(login_info.password.encode(),pw_from_db):
				raise HTTPException(status_code=404,detail='User not found(wrong password)')
			
			access_token = generate_token(
				payload =AccessTokenPayload(user_id = user_info_fetch['id'],**user_info_fetch).model_dump(),
			)	




			await cursor.close()
			await conn.close()

			return access_token




