from fastapi import FastAPI
from routes import MainRouter

app = FastAPI(title='User Service')
app.include_router(MainRouter)



