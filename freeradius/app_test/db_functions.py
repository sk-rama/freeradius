from sqlalchemy.orm import Session
import ipaddress

from . import models_db as model

def get_max_id_from_column(db_session: Session, model_column: str):
    result = db_session.query(model_column).all()
    result = [value for value, in result]
    return max(result)

def get_next_ip_address(db_session):
    last_ip_list = db_session.query(model.RadReply).order_by(model.RadReply.id.desc()).limit(1)
    last_ip = last_ip_list[0].value
    ip = ipaddress.ip_address(last_ip)
    if str(ip).endswith('254'):
        return str(ip + 3)
    else:
        return str(ip + 1)    