from fastapi import Depends, FastAPI, HTTPException
import logging

import crud
from schema import AccessData
from database import db
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.post("/access")
async def access(access_item: AccessData, access_db: Session = Depends(db.get_session)):
    logging.info("access")
    
    user = crud.check_user_in_db(access_item.user_id, access_db)
    if user is None:
        raise HTTPException(status_code=403, detail="접근이 거부되었습니다. 유저가 존재하지 않습니다.")
    
    crud.write_access_data_in_db(access_item, access_db)
    return {"message": f"환영합니다, {access_item.user_id}님!"}
    
@app.get("/ioc")
async def ioc(access_db: Session = Depends(db.get_session)):
    ioc = crud.get_ioc_in_db(access_db)
    if ioc is None:
        raise HTTPException(status_code=404, detail="IoC가 존재하지 않습니다.")
    else:
        return ioc