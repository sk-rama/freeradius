import sqlalchemy as db
from .database import Base

class RadCheck(Base):
    __tablename__ = 'radcheck'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    attribute = db.Column(db.String, default = 'Password')
    op = db.Column(db.String, default = '==')
    value = db.Column(db.String, default = 'password')
 
    def __repr__(self):
        return(f"RadCheck(id={self.id}, username={self.username}, attribute={self.attribute}, op={self.op}, value={self.value})\n")



class RadReply(Base):
    __tablename__ = 'radreply'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    attribute = db.Column(db.String, default='Framed-IP-Address')
    op = db.Column(db.String, default='=')
    value = db.Column(db.String, default='0.0.0.0')

    def __repr__(self):
        return(f"RadCheck(id={self.id}, username={self.username}, attribute={self.attribute}, op={self.op}, value={self.value})\n")



class RadUserGroup(Base):
    __tablename__ = 'radusergroup'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    groupname = db.Column(db.String, default = 'secar')
    priority = db.Column(db.Integer, default = 1)

    def __repr__(self):
        return(f"RadUserGroup(id={self.id}, username={self.username}, groupname={self.groupname}, priority={self.priority})\n")