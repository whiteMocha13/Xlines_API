from fastapi import FastAPI
from pydantic import BaseModel

class XLineColorUpdate(BaseModel):
    code:int
    color:str 
