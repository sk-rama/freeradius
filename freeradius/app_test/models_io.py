from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UserOut(BaseModel):
    id: int
    name = str
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    ts: datetime = None

    @validator('ts', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now()