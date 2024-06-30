from pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class User(BaseModel):
    login: str
    password: str 


class warningZone(BaseModel):
    xCoord: float
    yCoord: float
    typeZone: str
    distance: float
    #secret_key: str


class userPosition(BaseModel):
    xCoord: float
    yCoord: float
    #secret_key: str


class userInfo(BaseModel):
    user: str
    currentSpeed: float
    xCoord: float
    yCoord: float
    allowedSpeed: float
    #secret_key: str

class trackInfo(BaseModel):
    user_id: str
    currentSpeed: float
    xCoord: float
    yCoord: float
    track_id: int
    #secret_key: str