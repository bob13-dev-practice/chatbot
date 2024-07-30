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
    print(user)
    if user is None:
        # 사용자 조회 후 거부
        raise HTTPException(status_code=403, detail="접근이 거부되었습니다. 유저가 존재하지 않습니다.")
    
    crud.write_access_data_in_db(access_item, access_db)
    
    # 사용자 접근 허용
    return {"message": f"환영합니다, {access_item.user_id}님!"}