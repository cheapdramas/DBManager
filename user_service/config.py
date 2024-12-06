import dotenv

ENV:dict = dotenv.dotenv_values('.env')

class DatabaseConfig:
	user     =    ENV['DATABASE_USER']
	password =    ENV['DATABASE_PASSWORD']
	database =    ENV['DATABASE_NAME']
	host     =    ENV['DATABASE_HOST']
	port     =    ENV['DATABASE_PORT']
	DSN      =    f'postgresql://{host}/{database}?user={user}&password={password}'
