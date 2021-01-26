import uvicorn
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

from app_radius1 import routes_items

app = FastAPI()

app.include_router(routes_items.router, prefix="/radius1")

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)