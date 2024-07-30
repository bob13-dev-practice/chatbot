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


def check_user_in_db(user_id: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_ioc_in_db(db: Session) -> Optional[IoCData]:
    iocs = db.query(IoC).filter().all()
    if iocs:
        return [IoCData.model_validate(ioc) for ioc in iocs]
    return None