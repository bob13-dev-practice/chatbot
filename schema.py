from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AccessData(BaseModel):
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    access_time: Optional[datetime] = None
    access_id: Optional[str] = None

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위해 설정

class IoCData(BaseModel):
    ioc_item: Optional[str] = None
    ioc_type: Optional[str] = None

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위해 설정
        # from_attributes = True

class BobWikiData(BaseModel):
    id: int
    user_name: str
    age: Optional[int] = None
    hometown: Optional[str] = None
    contents: Optional[str] = None

    class Config:
        orm_mode = True  # ORM 모델과의 호환성을 위해 설정
        from_attributes = True