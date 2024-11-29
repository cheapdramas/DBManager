from fastapi import FastAPI
import uvicorn
app = FastAPI(title='DBManager')


print('hello world')

if __name__ == '__main__':
	uvicorn.run('main:app',reload=True)
