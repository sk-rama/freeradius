from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UserOut(BaseModel):
    id: int
    name: str
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    ts: datetime = None

    @validator('ts', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now()

class TelNumberOut(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None   
    value: Optional[str] = None 

    class Config:
        orm_mode = True

class TelNumberIn(BaseModel):
     username: Optional[str] = None

     @validator('username', pre=True, always=True)
     def is_tel_number(cls, v):
        if v[0:3] != '420':
            raise ValueError('must start with string 420')
        if len(v) != 12:
            raise ValueError('must contain 12 numbers')
        return v

