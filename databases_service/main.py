from fastapi import FastAPI
from routes import MainRouter


app = FastAPI(title='Databases Service')
app.include_router(MainRouter)

	
