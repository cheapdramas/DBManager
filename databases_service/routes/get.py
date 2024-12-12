from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def greetings():
	return 'Hello!'


