from pydantic import BaseModel,Field,AfterValidator
from uuid import uuid4
from typing import Annotated
import json
class ModelDependencies():
	@staticmethod
	def generate_uuid() -> str:
		return str(uuid4())
	@staticmethod
	def convert_to_json(value:dict) -> str:
		json_str = json.dumps(value)
		return json_str



class DBModel(BaseModel): #we will use this model only for appending new databases
	id:Annotated[str,Field(default_factory=ModelDependencies.generate_uuid)] 
	db_name:str
	db_system:str
	connection_info:Annotated[dict,AfterValidator(ModelDependencies.convert_to_json)]
	user_id:str #to which user will it belong

class DBCreationModel(BaseModel):
	db_name:str
	db_system:str
	connection_info:dict
	user_id:str
	




