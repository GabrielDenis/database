from fastapi import FastAPI
from fastapi import HTTPException

from database import User
from database import database as connection

from schemas import UserRequestModel
from schemas import UserResponseModel

app = FastAPI(
    title='Prueba de API',
    description='Esto es una prueba de API',
    version='1.0.0'
)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()

@app.get('/')
async def index():
    return 'Hola Mundo!'

@app.post('/users')
async def create_user(user_request: UserRequestModel):
    user = User.create(
        username=user_request.username,
        email=user_request.email
    )
    return user_request

@app.get('/users/{user_id}')
async def get_user(user_id):
    user = User.select().where(User.id == user_id).first()

    if user:
        return UserResponseModel(id=user.id, username=user.username, email=user.email)

    else:
        return HTTPException(404, 'User not found')

@app.delete('/users/{user_id}')
async def delete_user(user_id):
    user = User.select().where(User.id == user_id).first()

    if user:
        user.delete_instance()
        return True

    else:
        return HTTPException(404, 'User not found')