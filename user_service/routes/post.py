import bcrypt
import psycopg
from fastapi import APIRouter,HTTPException,status
from psycopg.rows import dict_row
from models.user import UserRegister,User,UserLogin
from models.tokens import AccessTokenPayload,RefreshTokenPayload
from models.responses import TokenInfo
from config import DatabaseConfig,TokenConfig
import auth as auth_utils
from .get import RouteHelpersFuncs as RouteHelpersFuncs_get

router = APIRouter()


@router.post('/register')
async def register_user_route(user_info:UserRegister) -> None:
	await RouteHelpersFuncs().add_user(user_info)
		
@router.post('/login',response_model=TokenInfo)
async def login_user_route(login_info:UserLogin):
	
	logined_user_info:dict  = await RouteHelpersFuncs().login_user(login_info)
	logined_user_id:str = logined_user_info['id']

	access_token = auth_utils.generate_access_token(
		payload=AccessTokenPayload(user_id=logined_user_id,**logined_user_info).model_dump()
	)
	refresh_token = auth_utils.generate_refresh_token(
		payload=RefreshTokenPayload(user_id=logined_user_id).model_dump()
	)

	return TokenInfo(
		access_token=access_token,
		refresh_token=refresh_token
	)

@router.post('/refresh_token',response_model=TokenInfo,response_model_exclude_none=True) #not sure about this endpoint in USER sevice, this is more about auth
async def refresh_access_token_route(refresh_token:str):
	access_token = await RouteHelpersFuncs().refresh_access_token(refresh_token)	
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
			try:
				await cursor.execute(sql_query,params=sql_parameters)
				await conn.commit()

				await cursor.close()
				await conn.close()
			except Exception as ex:
				raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(ex))
	@staticmethod
	async def login_user(login_info:UserLogin) ->dict:
		sql_query = """
			SELECT * FROM users WHERE login = %s
		"""			
		sql_parameters = (
			login_info.login,
		)		

		async with await RouteHelpersFuncs().connect_to_db(row_factory=dict_row) as conn:
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


			await cursor.close()
			await conn.close()

			return user_info_fetch


	@staticmethod
	async def refresh_access_token(refresh_token:str) -> str:
		try:
			refresh_token_payload =  auth_utils.decode_token(refresh_token)
			if refresh_token_payload.get('type') != 'refresh':
				raise HTTPException(status_code=400,detail='Invalid Token Type For Refreshing')
		except Exception as ex:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(ex))
		#if we are here, than our refresh token is valid

		user_info:dict = await RouteHelpersFuncs_get().get_user_info(refresh_token_payload['user_id'])
		if user_info == None:
			raise HTTPException(status_code=404,detail='User not found')

		access_payload:dict = AccessTokenPayload(
			user_id = user_info['id'],
			**user_info
		).model_dump()
		return auth_utils.generate_access_token(access_payload) 
