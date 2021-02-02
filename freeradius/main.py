import uvicorn
from functools import lru_cache
import config
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

import app_test.routes_items


@lru_cache()
def get_settings():
    return config.Settings()

app = FastAPI()

app.include_router(app_test.routes_items.router, prefix="/radius1")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):    
    return item

@app.get("/")
async def root():
    return {"message": "Hello World2"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):    
    return {"item_id": item_id}

@app.get("/info/")
async def get_info():
    settings = get_settings()
    return settings.app_name    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)