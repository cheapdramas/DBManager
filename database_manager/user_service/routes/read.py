from fastapi import APIRouter
import psycopg
from psycopg.connection_async import AsyncConnection
from config import DatabaseConfig



router = APIRouter()




@router.get('/test_db')
async def testing_database():
	return str((await RouteHelpersFuncs().get_all_from_table_test(),await RouteHelpersFuncs.connect_to_db()))






def RouteHelpersFuncs(): #proxy function for accessing class that i wrote below endpoints just because
	return RouteHelpersFuncs()
class RouteHelpersFuncs():
	@staticmethod
	async def connect_to_db() -> AsyncConnection:
		conninfo = f"""
			host={DatabaseConfig.host} 
			dbname={DatabaseConfig.database} 
			user={DatabaseConfig.user} 
			password={DatabaseConfig.password} 
		"""
		connection = await psycopg.AsyncConnection.connect(conninfo=conninfo)
		return connection

	@staticmethod
	async def get_all_from_table_test():
		async with await RouteHelpersFuncs.connect_to_db() as conn:
			cursor = conn.cursor()

			await cursor.execute('SELECT * FROM test_table')
			result = await cursor.fetchone()
			return result
	