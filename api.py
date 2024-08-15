from fastapi import Depends, FastAPI, HTTPException
import logging

import crud
from schema import AccessData, IoCData
from database import db
from sqlalchemy.orm import Session
from vt import virustotal
from ctx import ctx

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
    # return {"message": f"환영합니다, {access_item.user_id}님!"}
    return True
    
@app.post("/ioc/virustotal")
async def ioc(ioc: IoCData):
    logging.info("IOC_DATA API")
    return virustotal(ioc.ioc_item, ioc.ioc_type)

@app.post("/ioc/ctx")
async def ioc(ioc: IoCData):
    logging.info("IOC_DATA API")
    return ctx(ioc.ioc_item, ioc.ioc_type)


@app.get("/bob-wiki")
async def bob_wiki(db: Session = Depends(db.get_session)):
    logging.info("BOB WIKI API")
    bob_wiki_data = crud.get_bob_wiki_in_db(db)
    return bob_wiki_data