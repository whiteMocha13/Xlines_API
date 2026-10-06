import sqlite3
from fastapi import FastAPI, HTTPException, Depends 
from models import XLineColorUpdate, XLine
from database import get_db, init_db

init_db()
app = FastAPI()

@app.get("/xline/")
async def get_all_xline(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM xlines").fetchall()
    return [dict(row) for row in rows] 


@app.get("/xline/{xline_code}")
async def get_xline(xline_code: int, db:sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        "SELECT * FROM xlines WHERE code = ?",
        (xline_code,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="X-Line not found")
    return dict(row)

@app.post("/xline/")
async def create_xline(xline: XLine, db:sqlite3.Connection = Depends(get_db)):
    existing = db.execute(
        "SELECT * FROM xlines WHERE code = ?", (xline.code,),).fetchone()
    if existing is not None:
        raise HTTPException(status_code=400, detail="X-Line already exists.")
    db.execute(
        """
        INSERT INTO xlines(code, color, price, tax_percent, stock, is_active, shipping_weight)
        VALUES(?,?,?,?,?,?,?)
        """
        ,
        (
            xline.code,
            xline.color,
            xline.price,
            xline.tax_percent,
            xline.stock,
            int(xline.is_active), #SQLite bool tipi yok. İnt göndermek daha doğru. 0-1 olarak.
            xline.shipping_weight,
        ),
    )
    db.commit()
    return xline

@app.delete("/xline/{xline_code}")
async def del_xline(xline_code:int, db: sqlite3.Connection = Depends(get_db)):
    exists = db.execute("SELECT * FROM xlines WHERE code = ?", (xline_code,)).fetchone()
    if exists is None: 
        raise HTTPException(status_code=404, detail="X-Line not found.")
    db.execute("DELETE FROM xlines WHERE code = ?", (xline_code,))
    db.commit()
    return {"deleted" : xline_code}
    

            

@app.put("/xline/color")
async def update_xline_color(body: XLineColorUpdate, db:sqlite3.Connection = Depends(get_db)):
    
    row = db.execute("SELECT * FROM xlines WHERE code = ?", (body.code,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"XLine with code {body.code} is not found.")
    
    db.execute("UPDATE xlines SET color = ? WHERE code = ?", (body.color, body.code),)
    db.commit()
    return {"code": body.code, "color": body.color}
    
    



