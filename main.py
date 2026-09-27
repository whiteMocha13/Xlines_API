from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from update_classes import XLineColorUpdate

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class XLine(BaseModel):
    code:int
    color:str
    price:float
    tax_percent:int 
    stock:int
    is_active:bool
    shipping_weight:float
    
xlines: list[XLine] = [
    XLine(
        code=1,
        color="Iron Gray",
        price=1200.0,
        tax_percent=20,
        stock=50,
        is_active=True,
        shipping_weight=40.5,
    ),
    XLine(
        code=2,
        color="Traffic Red",
        price=1200.0,
        tax_percent=20,
        stock=50,
        is_active=True,
        shipping_weight=40.5,
    ),
    XLine(
        code=3,
        color="Sky Blue",
        price=1200.0,
        tax_percent=20,
        stock=50,
        is_active=True,
        shipping_weight=40.5,
    ),
]
app = FastAPI()

@app.get("/xline/")
async def get_all_xline():
    return xlines 


@app.get("/xline/{xline_code}")
async def get_xline(xline_code: int):
    for item in xlines:
        if xline_code == item.code:
            return item
    raise HTTPException(status_code=404, detail="X-Line not found")


@app.post("/xline/create/")
async def create_xline(xline: XLine):
    for item in xlines: 
        if item.code == xline.code: 
                raise HTTPException(status_code=400, detail="X-Line already exists.")
    xlines.append(xline)
    return xline

@app.delete("/xline/delete/{xline_code}")
async def del_xline(xline_code:int):
    for item in xlines:
        if item.code == xline_code:
            xlines.remove(item)
            return{
                "message": f"X-Line with code {xline_code} is deleted.",
                "deleted": item,
            }
    raise HTTPException(status_code=404, detail="X-Line not found.")

            

@app.put("/xline/update/color")
async def update_xline_color(body: XLineColorUpdate):
    for item in xlines:
        if item.code == body.code:
            item.color = body.color
            return item
    raise HTTPException(status_code=404, detail=f"XLine with code {body.code} is not found.")



