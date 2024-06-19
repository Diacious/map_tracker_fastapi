import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI
from gotrue.errors import AuthApiError
from pydantic import BaseModel

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

supabase = create_client(url, key)

app = FastAPI()

class User(BaseModel):
    login: str
    password: str 


class warningZone(BaseModel):
    xCoord: float
    yCoord: float
    typeZone: str
    distance: float
    secret_key: str


class userPosition(BaseModel):
    xCoord: float
    yCoord: float
    secret_key: str


class userInfo(BaseModel):
    user: str
    currentSpeed: float
    xCoord: float
    yCoord: float
    allowedSpeed: float
    secret_key: str



# Регистрация пользователя
@app.post("/users/sign-up")
async def create_user(user: User):
    
    credentials = {
    "email": user.login,
    "password": user.password
    }
    
    # TODO добавить обработку различных исключение при регистрации
    try:
        #user, session = supabase.auth.sign_up(credentials)
        session = supabase.auth.sign_up(credentials)
    except AuthApiError as e:
        return AuthApiError.to_dict(e)

    #res = {'status': 200,
    #       'user': user[1]}
    
    return session
    #return res, session


@app.post("/users/sign-out")
async def log_out():
    res = supabase.auth.sign_out()

    return {"status": 200,
            "res": res}

# Получение информации о текущей сесссии
@app.get("/users/session")
async def get_session():
    res = supabase.auth.get_session()
    
    return {"status": 200,
            "res": res}

# Получение информации о текущем пользователе 
@app.get("/users/user")
async def get_user():
    res = supabase.auth.get_user()
    
    return {"status": 200,
            "res": res}


# Вход пользователя
@app.post("/users/sign-in")
async def log_in(user: User):

    credentials = {
    "email": user.login,
    "password": user.password
    }

    # TODO добавить обработку различных исключение при входе пользователя
    try:
        #user, session = supabase.auth.sign_in_with_password(credentials)
        session = supabase.auth.sign_in_with_password(credentials)
    except AuthApiError as e:
        return AuthApiError.to_dict(e)

    #res = {'status': 200,
    #       'user': user[1]}

    return session
    #return res, session


# добавление записи об опасной зоне
@app.post("/warningZone/add")
async def add_warning_zone(warningZone: warningZone):
    assert warningZone.secret_key == SECRET_KEY, "Wrong secret key"
    data = supabase.table("warningZone").insert({"xCoord": warningZone.xCoord, "yCoord": warningZone.yCoord, "typeZone": warningZone.typeZone, "distance": warningZone.distance}).execute()
    assert len(data.data) > 0
    x_p = warningZone.xCoord + warningZone.distance
    x_m = warningZone.xCoord - warningZone.distance
    y_p = warningZone.yCoord + warningZone.distance
    y_m = warningZone.yCoord - warningZone.distance
    data_coord = supabase.table('coord').insert({"id_coord": data.data[0]['id'],"x_p": x_p, "x_m": x_m, "y_p": y_p, "y_m": y_m}).execute()
    #print(data_coord)
    assert len(data_coord.data) > 0


@app.post("/warningZone/get")
async def get_warning_zone(userPosition: userPosition):
    assert userPosition.secret_key == SECRET_KEY, "Wrong secret key"
    data = supabase.table('coord').select('id_coord', count='exact').filter('x_p', 'gte', userPosition.xCoord).filter('x_m', 'lte', userPosition.xCoord).filter('y_p', 'gte', userPosition.yCoord).filter('y_m', 'lte', userPosition.yCoord).execute()
    if data.count > 0:
        count = data.count
        data_responce = ''
        for i in range(0, count):
            data_ = supabase.table('warningZone').select('*').filter('id', 'eq', data.data[0]['id_coord']).execute()
            if i == 0:
                data_responce = data_
            else:
                data_responce = data_responce + ' ' + data_
        return data_responce
    else:
        res = {'status': 200}
        return res
    

@app.post("/userInfo/add")
async def add_user_info(userInfo: userInfo):
    assert userInfo.secret_key == SECRET_KEY, "Wrong secret key"
    data = supabase.table("userInfo").insert({"user": userInfo.user, "currentSpeed": userInfo.currentSpeed, "xCoord": userInfo.xCoord, "yCoord": userInfo.yCoord, "allowedSpeed": userInfo.allowedSpeed}).execute()
    assert len(data.data) > 0