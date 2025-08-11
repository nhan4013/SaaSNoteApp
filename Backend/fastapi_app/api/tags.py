from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import AuthUser
from schemas import TagOut, TagIn
from dependencies import get_current_user
from crud import tags as crud_tags

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.get("/", response_model=list[TagOut])
def list_tags(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    return crud_tags.list_tags(db, current_user)


@tags_router.post("/", response_model=TagOut)
def create_tag(
    tag: TagIn,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    return crud_tags.create_tag(tag, db, current_user)


@tags_router.put("/{id}", response_model=TagOut)
def update_tag(
    id: int,
    tag: TagIn,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    return crud_tags.create_tag(id, tag, db, current_user)
