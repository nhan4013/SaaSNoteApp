from fastapi import  Depends,APIRouter
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppTags, AuthUser
from .schemas import TagOut, TagIn
from .dependencies import get_current_user
from fastapi import status,HTTPException
from datetime import datetime,timezone

tags_router = APIRouter(prefix="/tags", tags=["tags"])

@tags_router.get("/",response_model=list[TagOut])
def list_tags(
    db:Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    tags = db.query(AppTags).filter(AppTags.user_id==current_user.id).all()
    
    return tags

@tags_router.post("/",response_model=TagOut)
def create_tag(
    tag: TagIn,
    db:Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    new_tag = AppTags(name=tag.name,user_id=current_user.id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@tags_router.put("/{id}",response_model=TagOut)
def create_tag(
    id:int,
    tag: TagIn,
    db:Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    tag_update = db.query(AppTags).filter(
        AppTags.id == id,
        AppTags.user_id == current_user.id
    ).first()
    if not tag_update :
        raise HTTPException(status_code=404,detail="Tag not found")
    tag_update.name = tag.name
    db.commit()
    db.refresh(tag_update)
    return tag_update