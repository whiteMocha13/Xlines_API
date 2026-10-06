from pydantic import BaseModel

class XLineColorUpdate(BaseModel):
    code:int
    color:str 

class XLine(BaseModel):
    code:int
    color:str
    price:float
    tax_percent:int 
    stock:int
    is_active:bool
    shipping_weight:float
    