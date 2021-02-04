from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List
import ipaddress

from . import models_db

def get_max_id_from_radcheck(db_session: Session):
    result = db_session.query(models_db.RadCheck.id).all()
    result = [value for value, in result]
    return max(result)

def get_max_id_from_radreply(db_session: Session):
    result = db_session.query(models_db.RadReply.id).all()
    result = [value for value, in result]
    return max(result)

def get_max_id_from_radusergroup(db_session: Session):
    result = db_session.query(models_db.RadUserGroup.id).all()
    result = [value for value, in result]
    return max(result)  

def test_same_max_id(db_session: Session):
    return True if get_max_id_from_radcheck(db_session) == get_max_id_from_radreply(db_session) == get_max_id_from_radusergroup(db_session) else False      

def exist_in_db(db_session: Session, numbers: List[str]):
    try:
        for number in numbers:
            query1 = db_session.query(exists().where(models_db.RadCheck.username == str(number))).scalar()
            query2 = db_session.query(exists().where(models_db.RadReply.username == str(number))).scalar()
            query3 = db_session.query(exists().where(models_db.RadUserGroup.username == str(number))).scalar()
            print(query1)
            if query1 or query2 or query3:
                print(f'\n \033[0;31m tel. cislo {number} se uz v databaze nachazi !!! \033[0m \n')
                return True
        return False
    except:
        print('Nastala chyba')

def get_number_from_radreply(db_session, tel_number:str):
    result = db_session.query(models_db.RadReply).filter(models_db.RadReply.username==tel_number).first()
    return result          

def get_next_ip_address(db_session: Session):
    last_ip_list = db_session.query(models_db.RadReply).order_by(models_db.RadReply.id.desc()).limit(1)
    last_ip = last_ip_list[0].value
    ip = ipaddress.ip_address(last_ip)
    if str(ip).endswith('254'):
        return str(ip + 3)
    else:
        return str(ip + 1)    

def add_to_db(db_session: Session, tel_number: str):
    try:
        if test_same_max_id(db_session):
            id = get_max_id_from_radcheck(db_session) + 1

            model_1 = models_db.RadCheck(id = id, username = str(tel_number))
            model_2 = models_db.RadReply(id = id, username = str(tel_number), value = get_next_ip_address(db_session))
            model_3 = models_db.RadUserGroup(id = id, username = str(tel_number))

            db_session.add(model_1)
            db_session.add(model_2)
            db_session.add(model_3)
    except: 
        db_session.rollback()
        return False
    else:  
        db_session.commit()
        return True
