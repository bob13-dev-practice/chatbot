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