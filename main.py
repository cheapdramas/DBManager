from fastapi import FastAPI
import uvicorn
app = FastAPI(title='DBManager')




if __name__ == '__main__':
	uvicorn.run('main:app',reload=True)
