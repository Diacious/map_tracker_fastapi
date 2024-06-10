import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI
from gotrue.errors import AuthApiError
from pydantic import BaseModel

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

app = FastAPI()

class User(BaseModel):
    login: str
    password: str 



# Регистрация пользователя
@app.post("/users/sign-up")
async def create_user(user: User):
    
    credentials = {
    "email": user.login,
    "password": user.password
    }
    
    # TODO добавить обработку различных исключение при регистрации
    try:
        user, session = supabase.auth.sign_up(credentials)
    except AuthApiError as e:
        return AuthApiError.to_dict(e)

    res = {'status': 200,
           'user': user[1]}
    

    return res


@app.post("/users/sign-out")
async def log_out():
    res = supabase.auth.sign_out()

    return {"status": 200}


# Вход пользователя
@app.post("/users/sign-in")
async def get_user(user: User):

    credentials = {
    "email": user.login,
    "password": user.password
    }

    # TODO добавить обработку различных исключение при входе пользователя
    try:
        user, session = supabase.auth.sign_in_with_password(credentials)
    except AuthApiError as e:
        return AuthApiError.to_dict(e)

    res = {'status': 200,
           'user': user[1]}

    return res