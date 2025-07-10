from datetime import datetime
from pydantic import BaseModel

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True
        
class NoteIn(BaseModel):
    title:str
    content:str