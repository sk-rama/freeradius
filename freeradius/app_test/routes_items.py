from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Optional, List
import re

from sqlalchemy.orm import Session
from .database import SessionLocal
from . import db_functions as fnct
from . import models_io 

router = APIRouter()

fake_users = { "user1": {"id": 1, "password": "pass1", "name": "Prvni Jmeno", "company": "company1", "email": "email@email.cz"}, 
               "user2": {"id": 2, "password": "pass2", "name": "Druhe Jmeno", "company": "company2", "email": "email@email.cz"}
} 

def validate_tel_number(tel_number: str) -> bool:
    if tel_number[0:3] != '420':
        raise HTTPException(status_code=404, detail='Tel. Number must start with string 420')
    if len(tel_number) != 12:
        raise HTTPException(status_code=404, detail='Tel. Number must contain 12 numbers')
    if len(tel_number) != len(re.match('[0-9]*', tel_number).group(0)):
        raise HTTPException(status_code=404, detail='Tel. Number must contain only numbers')
    return True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tel_number/{tel_number}", response_model=models_io.TelNumberOut)
async def get_number_from_db(tel_number: str, db: Session = Depends(get_db)):
    if validate_tel_number(tel_number=tel_number):
        result = fnct.get_number_from_radreply(db_session=db, tel_number=tel_number)
        if result is None:
            raise HTTPException(status_code=404, detail='Tel. Number not found')
        else:
            return result

@router.post("/tel_number/{tel_number}")
async def add_number_to_db(tel_number: str, db: Session = Depends(get_db)):
    if validate_tel_number(tel_number=tel_number):
        if fnct.exist_in_db(db_session=db, numbers=tel_number.split()):
            raise HTTPException(status_code=404, detail='Tel. Number exist in database') 
        else:   
            fnct.add_to_db(db_session=db, tel_number=tel_number)
            return {tel_number: "True"} 
    else:
        return {tel_number: "False"}

@router.post("/tel_numbers/")
async def add_list_of_tel_numbers_to_db(tel_numbers: models_io.TelNumbersIn, db: Session = Depends(get_db)):
    # convert models_io.TelNumbersIn Pydantic model to dict()
    tel_numbers = tel_numbers.dict()
    # remove duplicates from dict tel_numbers and key tel_numbers
    tel_numbers = list(set(tel_numbers["tel_numbers"]))
    # remove tel. numbers exists in db 
    unique_numbers = [item for item in tel_numbers if (not fnct.exist_in_db(db_session=db, numbers=item.split()))]
    # add unique_numbers items to db and return dict where key is tel.number and value is True/False from function add_to_db(...)
    status = {item: fnct.add_to_db(db_session=db, tel_number=item) for item in unique_numbers}
    return status  
     

# @router.get("/getmaxid/RadCheck/")
# def get_max_id_from_radcheck(db: Session = Depends(get_db)):
#     max_id = fnct.get_max_id_from_radcheck(db_session=db)
#     return max_id   

# @router.get("/get_next_ipaddress/")
# def get_next_ip(db: Session = Depends(get_db)):
#     ip_address = fnct.get_next_ip_address(db_session=db)
#     return ip_address     


# @router.get("/")
# async def read_items():
#     return [{"name": "Item Foo"}, {"name": "item Bar"}]


# @router.get("/{item_id}", response_model=models_io.UserOut)
# async def read_item(item_id: str):
#     if item_id in fake_users:
#         return {**fake_users[item_id]}

# @router.get("/item/{item_id}")
# async def read_item(item_id: str, user_agent: Optional[str] = Header(None)):
#     if item_id in fake_users:
#         return {**fake_users[item_id], **{"User-Agent": user_agent}}


# @router.put("/{item_id}", tags=["custom"], responses={403: {"description": "Operation forbidden"}})
# async def update_item(item_id: str):
#     if item_id != "foo":
#         raise HTTPException(status_code=403, detail="You can only update the item: foo")
#     return {"item_id": item_id, "name": "The Fighters"}    