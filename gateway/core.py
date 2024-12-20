import aiohttp
from functools import wraps
import dotenv
import pathlib
import json


environ = dotenv.dotenv_values(pathlib.Path(__file__).parent/'services.env')


async def send_request(
	method:str,
	service:str,
	path:str,
	parameters:str,
	json_ = None,
):
	method=method.upper()
	service_url = environ[service.upper()]
	request_url = f'{service_url}/{path}{parameters}'
	
	

	async with aiohttp.ClientSession() as session:
		if method == "GET":
			async with session.get(request_url) as response:
				return await response.json()
		if method == "POST":
			async with session.post(request_url,json=json_) as response:
				return await response.json()
		if method == "PUT":
			async with session.put(request_url,json=json_) as response:
				return await response.json()
		if method == "DELETE":
			async with session.delete(request_url,json=json_) as response:
				return await response.json()



def route(
	method:str,
	service:str,
	path:str,
	parameter_in_route:str=None	
):
	def func_init(route_func):
		@wraps(route_func)
		async def wrap(**route_kwargs):
			parameters =''
			json = None
			path_ = path

			for k,v in route_kwargs.items():
				if type(v) == str or type(v) == int:
					if k == parameter_in_route:
						path_= path_.format(**{k:v})

					else:
						parameters += '?' + str(k) + '=' + str(v)
				else:
					json = v.model_dump()
					
			request = await send_request(
				method=method,
				service=service,
				path=path_,
				json_=json,
				parameters=parameters
			)			
			
			return request	

		return wrap

	return func_init
		