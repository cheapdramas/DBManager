import psycopg
from fastapi import APIRouter,HTTPException,status,Depends
from psycopg import sql
from psycopg.rows import dict_row
from config import MainDBConfig,DBClusterConfig
from models.models import DBRegistration
from auth import access_token,generate_uuid


router = APIRouter()



@router.post('/register_db')
async def register_db_route(db_info:DBRegistration):
	"Register database for user"
	await RouteHelperFuncs().register_db(db_info)

	return db_info




def RouteHelperFuncs():
	return RouteHelperFuncs()
class RouteHelperFuncs():
	@staticmethod 
	async def connect_to_mainDB(**kwargs) -> psycopg.connection_async.AsyncConnection:
		DSN = MainDBConfig.DSN 
		connection = await psycopg.AsyncConnection.connect(DSN,**kwargs)
		return connection
	
	@staticmethod 
	async def connect_to_DBcluster(**kwargs) -> psycopg.connection_async.AsyncConnection:
		DSN = DBClusterConfig.DSN
		connection = await psycopg.AsyncConnection.connect(DSN,**kwargs)
		return connection

	@staticmethod
	async def register_db(db_info:DBRegistration):
		db_id = generate_uuid()

		
		#TODO : somehow add statement that checks count with the same user_id, to prevent situation where user having more than 5 dbs
		sql_query = """
			INSERT INTO databases(
				id,
				db_name,
				db_system,
				password,
				user_id
			) 
			SELECT 
			
		"""
		sql_parameters = [
			db_id,
			*db_info.model_dump().values()
		]
		try:
			async with await RouteHelperFuncs.connect_to_mainDB() as conn:
				cursor = conn.cursor()
				
				await cursor.execute(sql_query,sql_parameters)
				await conn.commit()
	
				await conn.close()
				await cursor.close()
		except Exception as ex:
			raise HTTPException(400,detail=str(ex))