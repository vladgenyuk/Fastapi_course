import time
from typing import List, Optional

import fastapi
from redis import asyncio as aioredis
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Depends, Request, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from auth.base_config import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.models import User

from base_config import current_user, fastapi_users
from config import REDIS_HOST, REDIS_PORT

from operations.router import router as router_operation
from tasks.router import router as router_tasks
from pages.router import router as router_template
from chat.router import router as router_chat


app = FastAPI(title='Trading app')


async def get_async_session1():
    print("Getting session")
    session = 'Session123'
    yield session
    print('Terminate session')


@app.get('/test_depend1', tags=['depend'])
async def get_items(session=Depends(get_async_session1)):
    return {'id': 1}


async def pagination_parameters(limit: int = 10, skip: int = 3):
    return {'limit': limit, 'skip': skip}


@app.get('/test_depend2', tags=['depend'])
async def get_items(params: dict = Depends(pagination_parameters)):
    return {'id': 1}


class Paginator:
    def __init__(self, limit: int = 10, skip: int = 3):
        self.limit = limit
        self.skip = skip


@app.get('/test_depend3', tags=['depend'])
async def get_items_class(params: Paginator = Depends(Paginator)):
    return {'id': 1}


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if "super_cookie" not in request.cookies:
            raise fastapi.HTTPException(status_code=403, detail='Forbidden from me')
        return True


auth_guard_payments = AuthGuard('payments')


@app.get('/payments', tags=['depend'], dependencies=[Depends(auth_guard_payments)])
async def get_payments():
    return 'PAYMENTS!'


app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],#origins,
    allow_credentials=True,
    allow_methods=["GET", 'POST', 'PUT', 'OPTIONS', 'DELETE', 'PATCH'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Origin', 'Access-Control-Request-Method',
                   'Authorization'],
)

app.include_router(router_template)
app.include_router(router_chat)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)

# Further example functions!!


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


fake_users = [
    {'id': 1, "role": 'admin', 'name': ['vlad1']},
    {'id': 1, "role": 'admin', 'name': 'vlad2'},
    {'id': 3, "role": 'admin', 'name': 'vlad3'},
    {'id': 4, "role": 'admin', 'name': 'vlad3',
     'degree': [{'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'},
                {'id': 2, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}]},
]


@app.get('/users/{user_id}')#, response_model=List[User])
async def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


fake_trades = [
    {'id': 1, "user_id": 1, 'currency': 'BTC', 'side': 'buy', 'price': 123},
    {'id': 2, "user_id": 2, 'currency': 'BTC', 'side': 'buy', 'price': 222},
    {'id': 3, "user_id": 3, 'currency': 'BTC', 'side': 'buy', 'price': 333},
]


@app.get('/trades')
async def get_trades(limit: int = 2, offset: int = 1):
    return fake_trades[offset:][:limit]


fake_users2 = [
    {'id': 1, "status": 'admin'},
    {'id': 2, "status": 'admin'},
    {'id': 3, "status": 'admin'},
]


@app.post('/users/{user_id}')
async def change_status(user_id: int, new_status: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, fake_users2))[0]
    current_user['status'] = new_status
    return {'status': 200, 'data': current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
async def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, "data": fake_trades}


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anon"


@app.on_event('startup')
async def on_startup():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
