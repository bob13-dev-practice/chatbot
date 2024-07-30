import hashlib
import json
from logging import error
# import requests
from sqlalchemy.orm import Session

from models import *
from schema import *
from config import conf

def write_access_data_in_db(access_item: AccessData, db: Session):
    access_table = Access_Table(
        user_id = access_item.user_id,
        channel_id = access_item.channel_id,
        access_id = access_item.access_id,
        access_time = access_item.access_time,
    )
    db.add(access_table)
    db.commit()

    return access_table

def check_user_in_db(user_id: str, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        return {error: str(e), 'msg': '존재하지 않는 유저입니다.'}