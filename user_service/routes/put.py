import psycopg
import bcrypt
from fastapi import APIRouter,HTTPException
from models.user import User,UserUpdate
from config import DatabaseConfig

router = APIRouter()

@router.put('/user')
async def update_user_info_route(user_id:str,user_update:UserUpdate) -> None:
	await RouteHelpersFuncs().update_user(user_id,user_update)
	




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
	async def update_user(user_id:str,user_update:dict):
		async with await RouteHelpersFuncs().connect_to_db() as conn:
			
			
			cursor = conn.cursor()
			password_confirm = user_update['password_confirm']
			user_update.pop('password_confirm')


			async def confirm_user_password():
				await cursor.execute('SELECT password FROM users WHERE id=%s',params=(user_id,))		
				
				db_user_password = await cursor.fetchone()
				if db_user_password == None:
					raise HTTPException(404,'User not found')
				db_user_password:bytes = db_user_password[0]

				password_for_confirmation:bytes = password_confirm.encode()
				if not bcrypt.checkpw(password_for_confirmation,db_user_password):
					raise HTTPException(status_code=404,detail='User password is not correct')
				
			async def generate_sql_request() -> str:				
				sql_request = 'UPDATE users SET '
				for index,column in enumerate(user_update):

					
					sql_request += f'{column} = %s'

					if index < len(user_update) -1:
						sql_request+=','

				
				sql_request += f' WHERE id=%s'
				return sql_request



			await confirm_user_password()	
			sql_request = await generate_sql_request()

			sql_parameters = [user_update[key] for key in user_update]
			sql_parameters.append(user_id)

			await cursor.execute(
				sql_request,
				params=sql_parameters
			)

			await conn.commit()
			await cursor.close()
			await conn.close()

