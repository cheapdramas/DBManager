from fastapi import FastAPI
from routes import MainRouter

app = FastAPI(title='API Gateway')
app.include_router(MainRouter)



