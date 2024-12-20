import psycopg
from fastapi import APIRouter, HTTPException
from psycopg import sql
from psycopg.rows import dict_row
from psycopg.connection_async import AsyncConnection
from psycopg.errors import UniqueViolation
from config import MainDBConfig, DBClusterConfig
from models.models import DBCreateModel
from auth import access_token, generate_uuid


router = APIRouter()




@router.post("/create_db")
async def create_db_route(access_token: access_token, db_info: DBCreateModel):
    """CREATE DATABASE"""
    user_id = access_token["user_id"]

    if db_info.db_system == "postgres":
        await RouteHelperFuncs().create_postgres_database(db_info,user_id)

    if db_info.db_system == "mongodb":
        pass

 

def RouteHelperFuncs():
    return RouteHelperFuncs()


class RouteHelperFuncs:
    @staticmethod
    async def connect_to_mainDB(**kwargs) -> AsyncConnection:
        DSN = MainDBConfig.DSN
        connection = await psycopg.AsyncConnection.connect(DSN, **kwargs)
        return connection

    @staticmethod
    async def connect_to_DBcluster(
        **kwargs,
    ) -> AsyncConnection:

        DSN = DBClusterConfig.DSN
        connection = await psycopg.AsyncConnection.connect(DSN, **kwargs)
        return connection

    @staticmethod
    async def register_db(db_info: DBCreateModel, user_id: str,database_connection:AsyncConnection):
        """Registrating new database, if successfull: function return just created database id"""

        db_id = generate_uuid()
        sql_query = sql.SQL(
            """
			DO $$
			BEGIN
				IF (SELECT count(*) FROM databases WHERE user_id = {user_id}) < 5 THEN
					INSERT INTO databases VALUES({db_id},{},{},{},{user_id});
                ELSE
                    RAISE EXCEPTION USING MESSAGE = 'User can`t have more than 5 databases!';
				END IF;
			END$$;	
		"""
        ).format(
            user_id=sql.Literal(user_id),
            db_id=sql.Literal(db_id),
            *list(map(lambda v: sql.Literal(v), db_info.model_dump().values())),
        )
        try:
            cursor = database_connection.cursor()            
            await cursor.execute(sql_query)
            await cursor.close()
            return db_id
        except Exception as ex:
            if ex == UniqueViolation: 
                raise HTTPException(409, detail="Error occured while registrating database  " + 'Database name already registered')
            raise HTTPException(400, detail="Error occured while registrating database  " + str(ex))



    @staticmethod 
    async def create_postgres_database(
        db_info:DBCreateModel,
        user_id:str
    ):
        sql_create_user = sql.SQL("""
            CREATE USER {db_id} WITH ENCRYPTED PASSWORD {db_password};
        """)      

        sql_create_database = sql.SQL(
            """CREATE DATABASE {db_name} OWNER {db_id};"""
        )




        async with await RouteHelperFuncs.connect_to_mainDB(autocommit=True) as conn:
            db_id = await RouteHelperFuncs.register_db(db_info,user_id,conn) #registered new database
            #formatting sql q
            sql_create_user=sql_create_user.format(
                db_id=sql.Identifier(db_id),
                db_password=sql.Literal(db_info.password)
            )
            sql_create_database=sql_create_database.format(
                db_name=sql.Identifier(db_info.db_name),
                db_id=db_id
            )

            #Executing sql queries
            cursor = conn.cursor()
            await cursor.execute(sql_create_user)
            await cursor.execute(sql_create_database)
            
            await cursor.close()
            await conn.close()
        return "Success"