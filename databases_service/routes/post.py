import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from fastapi import APIRouter,HTTPException,status
from config import MainDBConfig,DBClusterConfig
from models.models import DBModel,PGRegistrationModel

router = APIRouter()


@router.post('/register_pg')
async def register_postgres(pginfo:PGRegistrationModel):
	"""REGISTER NEW DATABASE"""
	full_info_db = await RouteHelperFuncs().register_pg(pginfo)

	return full_info_db.id


@router.post('/create_pg')
async def run_postgres(db_id:str):
	"""CREATING POSTGRES DATABASE (create database ...)"""
	await RouteHelperFuncs().create_pg(db_id)
	return 'success!'



	



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
	async def register_pg(pginfo:PGRegistrationModel):
		full_db_info = DBModel(
			db_name=pginfo.db_name,
			db_system='postgres',
			connection_info=pginfo.connection_info.model_dump(),
			user_id=pginfo.user_id
		)
		sql_query = """
			INSERT INTO databases(
				id,
				db_name,
				db_system,
				connection_info,
				user_id
			) VALUES (%s,%s,%s,%s,%s)
		"""
		sql_params = [i for i in full_db_info.model_dump().values()]
		
		async with await RouteHelperFuncs.connect_to_mainDB() as conn:
			cursor = conn.cursor()

			await cursor.execute(sql_query,sql_params)

			await conn.commit()
			await cursor.close()
			await conn.close()

		return full_db_info
			
			
	@staticmethod
	async def create_pg(pg_id:str):
		sql_query = """
			SELECT db_name,connection_info FROM databases WHERE id=%s
		"""
		sql_params = (pg_id,)

		async with await RouteHelperFuncs.connect_to_mainDB(row_factory=dict_row) as conn:
			cursor = conn.cursor()
			await cursor.execute(sql_query,sql_params)
			result:dict|None = await cursor.fetchone()
			if result == None:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Database not found')
			db_name = result['db_name']
			connection_info:str = result['connection_info']


			await cursor.close()
			await conn.close()		

		async with await RouteHelperFuncs.connect_to_DBcluster(autocommit=True) as cluster_conn:

		

			cursor = cluster_conn.cursor()


			await cursor.execute(
				sql.SQL('CREATE USER {} WITH ENCRYPTED PASSWORD {}').format(sql.Identifier(connection_info['postgres_user']),connection_info['postgres_password'])
			
			)


			await cursor.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(
					sql.Identifier(db_name),connection_info['postgres_user']
				)
			)
		
			await cursor.close()
			await cluster_conn.close()
		

		





		

