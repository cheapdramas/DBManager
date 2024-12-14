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

		sql_query = sql.SQL("""
			DO $$
			BEGIN
				IF (SELECT count(*) FROM databases WHERE user_id = {}) < 5 THEN
					INSERT INTO databases VALUES({},{},{},{},{});
				END IF;
			END$$;	
		""").format(
			sql.Literal(db_info.user_id),
			sql.Literal(db_id),
			*list(map(lambda v: sql.Literal(v),db_info.model_dump().values()))	
		)



		try:
			async with await RouteHelperFuncs.connect_to_mainDB(autocommit=True) as conn:
				cursor = conn.cursor()
				
				await cursor.execute(sql_query)
				
				await conn.close()
				await cursor.close()
		except Exception as ex:
			raise HTTPException(400,detail=str(ex))