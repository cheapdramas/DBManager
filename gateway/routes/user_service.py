from fastapi import APIRouter
from core import route
from models.user import UserRegister,UserLogin,UserUpdate

router = APIRouter(tags=['User Service'],prefix='/user')
USER_SERVICE="user_service"




@router.get('/users')
@route(
	'GET',
	USER_SERVICE,
	'user/users'
)
async def greetings():
	pass



@router.get('/user{user_id}')
@route(
	"GET",
	"user_service",
	"user/user{user_id}",
	"user_id"
)
async def get_user_route(user_id:str):
	pass



@router.post('/register')
@route(
	"POST",
	USER_SERVICE,
	"user/register"
)
async def user_register_route(user_info:UserRegister):
	pass

@router.post('/login')
@route(
	"POST",
	USER_SERVICE,
	"user/login"
)
async def user_login_route(creds:UserLogin):
	pass


@router.delete('/user')
@route(
	"DELETE",
	USER_SERVICE,
	"user/user/{access_token}",
	"access_token"
)
async def user_delete_route(access_token:str):
	pass


@router.put('/user{user_id}')
@route(
	"PUT",
	USER_SERVICE,
	"user/user{user_id}",
	"user_id"
)
async def update_user_route(user_id:str,user_update_info:UserUpdate):
	pass
