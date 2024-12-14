import dotenv
import pathlib
ENV:dict = dotenv.dotenv_values('.env')


class MainDBConfig:
	user     =    ENV['DATABASE_USER']
	password =    ENV['DATABASE_PASSWORD']
	database =    ENV['DATABASE_NAME']
	host     =    ENV['DATABASE_HOST']
	port     =    ENV['DATABASE_PORT']
	DSN      =    f'postgresql://{host}/{database}?user={user}&password={password}'

class DBClusterConfig:
	user     =    ENV['DATABASE_USER']
	password =    ENV['DATABASE_PASSWORD']
	database =    'postgres' #add to env
	host     =    ENV['DATABASE_HOST']
	port     =    ENV['DATABASE_PORT']
	DSN      =    f'postgresql://{host}/{database}?user={user}&password={password}'

class TokenConfig:
	public_key = (pathlib.Path(__file__).parent / 'certs' /'public.pem').read_text()
	algorithm = 'RS256'
	
