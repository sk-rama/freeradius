from fastapi import APIRouter, Header, Depends
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from .database import SessionLocal
from . import db_functions as fnct 

router = APIRouter()

fake_users = { "user1": {"id": 1, "password": "pass1", "name": "Prvni Jmeno", "company": "company1", "email": "email@email.cz"}, 
               "user2": {"id": 2, "password": "pass2", "name": "Druhe Jmeno", "company": "company2", "email": "email@email.cz"}
}  

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserOut(BaseModel):
    id: int
    name = str
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    ts: datetime = None

    @validator('ts', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now()


@router.get("/getmaxid/{db_id}")
def get_max_id(db_id:str, db: Session = Depends(get_db)):
    db_id = str(db_id)
    max_id = get_max_id_from_column(db_session=db, model_column=db_id)
    return users   

@router.get("/get_next_ipaddress/")
def get_next_ip(db: Session = Depends(get_db)):
    ip_address = fnct.get_next_ip_address(db_session=db)
    return ip_address     


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}", response_model=UserOut)
async def read_item(item_id: str):
    if item_id in fake_users:
        return {**fake_users[item_id]}

@router.get("/item/{item_id}")
async def read_item(item_id: str, user_agent: Optional[str] = Header(None)):
    if item_id in fake_users:
        return {**fake_users[item_id], **{"User-Agent": user_agent}}


@router.put("/{item_id}", tags=["custom"], responses={403: {"description": "Operation forbidden"}})
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}    