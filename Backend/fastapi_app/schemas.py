from datetime import datetime
from pydantic import BaseModel

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags:list[str]
    is_archived: bool = False
    class Config:
        orm_mode = True
        
class NoteIn(BaseModel):
    title:str
    content:str
    is_archived: bool = False
    tags:list[str] = []
    
class TagIn(BaseModel):
    name:str
    
class TagOut(BaseModel):
    id:int
    name:str
    user_id:int
    class Config:
        orm_mode = True
        
