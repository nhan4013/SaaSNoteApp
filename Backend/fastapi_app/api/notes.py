from fastapi import Depends, APIRouter, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from models import AuthUser
from schemas import NoteOut, NoteIn
from dependencies import get_current_user
from fastapi import status
from crud import notes as crud_notes
from utils.cache import redis_cache
from utils.limiter import limiter

notes_router = APIRouter(prefix="/notes", tags=["notes"])

# GET /notes/ — List all notes of the current user

def key_builder(*args, **kwargs):
    user = kwargs.get("current_user") or (args[1] if len(args) > 1 else None)
    return f"user:{user.id}:notes"


@notes_router.get("/", response_model=list[NoteOut])
@redis_cache(key_builder, expire=300)
@limiter.limit("20/minute")
async def list_notes(
    request: Request,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
    
):
    return await crud_notes.get_notes(db, current_user)

  # Get the note by ID and check if it belongs to the user

@limiter.limit("20/minute")
@notes_router.get("/{id}", response_model=NoteOut)
@redis_cache(key_builder, expire=300)
async def get_note(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)

):
    return await crud_notes.get_note_id(id, db, current_user)

# PUT /notes/{id} — Update a note

@limiter.limit("20/minute")
@notes_router.put("/{id}", response_model=NoteOut)
async def update_note(
    request: Request,
    id: int,
    note_in: NoteIn,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    return await crud_notes.update_note(id, note_in, db, current_user)

# DELETE /notes/{id} — Delete a note


@notes_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    return await crud_notes.delete_note(id, db, current_user)

# Create a new note for the current user


@notes_router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    return await crud_notes.create_node(note, db, current_user)

# Search notes by tag name or by title or content for the current user

@redis_cache(key_builder, expire=300)
@notes_router.get("/search", response_model=list[NoteOut])
async def search_notes_by_tag(
    tag: str = Query(..., description="Tag name to search for"),
    q: str = Query(..., description="Text to search in title or content"),
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)

):
    return await crud_notes.search_notes_by_tag(tag, q, db, current_user)

#
