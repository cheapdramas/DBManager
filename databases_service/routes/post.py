from fastapi import APIRouter
import psycopg
from config import MainDBConfig
from models.models import DBCreationModel,DBModel

router = APIRouter()


@router.post("/create_db")
async def db_creation_route(new_db_info: DBCreationModel):
	await RouteHelperFuncs().create_new_db(new_db_info)

	return 'Success!'


	







def RouteHelperFuncs():
	return RouteHelperFuncs()
class RouteHelperFuncs():
	@staticmethod 
	async def connect_to_mainDB(**kwargs) -> psycopg.connection_async.AsyncConnection:
		DSN = MainDBConfig.DSN 
		connection = await psycopg.AsyncConnection.connect(DSN,**kwargs)
		return connection
	@staticmethod 
	async def create_new_db(db_info:DBCreationModel):
		full_db_info = DBModel(**db_info.model_dump())
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
			
			
		
		

		
