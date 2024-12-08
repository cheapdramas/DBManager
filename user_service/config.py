import dotenv
import pathlib
from datetime import timedelta
ENV:dict = dotenv.dotenv_values('.env')


class DatabaseConfig:
	user     =    ENV['DATABASE_USER']
	password =    ENV['DATABASE_PASSWORD']
	database =    ENV['DATABASE_NAME']
	host     =    ENV['DATABASE_HOST']
	port     =    ENV['DATABASE_PORT']
	DSN      =    f'postgresql://{host}/{database}?user={user}&password={password}'

class TokenConfig:
	private_key = (pathlib.Path(__file__).parent / 'certs' /'private.pem').read_text()
	public_key = (pathlib.Path(__file__).parent / 'certs' /'public.pem').read_text()
	algorithm = 'RS256'
	class AccessToken:
		expire_min=timedelta(minutes=1)  #3
	class RefreshToken:
		expire_min=timedelta(minutes=2)