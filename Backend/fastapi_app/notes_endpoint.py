from fastapi import  Depends,APIRouter,Query
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppNotes, AuthUser ,AppTags
from .schemas import NoteOut, NoteIn
from .dependencies import get_current_user
from fastapi import status,HTTPException
from datetime import datetime,timezone

notes_router = APIRouter(prefix="/notes", tags=["notes"])

#GET /notes/ — List all notes of the current user
@notes_router.get("/", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    # Query notes that belong to the current user
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == current_user.id).all()

    return notes

 # Get the note by ID and check if it belongs to the user
@notes_router.get("/{id}", response_model=NoteOut)
def get_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)

):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == current_user.id
    ).first()
    if not note :
        raise HTTPException(status_code=404,detail="Note not found")
    return note

# PUT /notes/{id} — Update a note
@notes_router.put("/{id}",response_model=NoteOut)
def update_note(
    id:int,
    note_in:NoteIn,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    note.title = note_in.title
    note.content = note_in.content
    note.updated_at = datetime.now(timezone.utc)
    note.app_notes_tags.clear()
    db.commit()
    for tag_name in note_in.tags:
        tag = db.query(AppTags).filter_by(name=tag_name,user_id=current_user.id).first()
        if not tag:
            tag = AppTags(name=tag_name,user_id=current_user.id)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        note.app_notes_tags.append(tag)
    db.commit()
    db.refresh(note)
    return note

# DELETE /notes/{id} — Delete a note
@notes_router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_note(
    id:int,
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": f"Note {id} deleted successfully"}

# Create a new note for the current user
@notes_router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteIn, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    new_note = AppNotes(
        title=note.title, content=note.content, user_id=current_user.id, created_at=now,
        updated_at=now)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    for tag_name in note.tags:
        tag = db.query(AppTags).filter_by(name=tag_name,user_id=current_user.id).first()
        if not tag:
            tag = AppTags(name=tag_name,user_id=current_user.id)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        new_note.app_notes_tags.append(tag)
        db.commit()
        db.refresh(new_note)
    return new_note

# Search notes by tag name for the current user
@notes_router.get("/search",response_model=list[NoteOut])
def search_notes_by_tag(
    tag: str = Query(...,description="Tag name to search for"),
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
    
):
    notes = (
        db.query(AppNotes).join(AppNotes.app_notes_tags)
        .filter(
            AppNotes.user_id == current_user.id,
            AppTags.name == tag
        ).all()
        
    )
    return notes

# Full-text search notes by title or content for the current user
@notes_router.get("/search",response_model=list[NoteOut])
def search_notes_by_tag(
    q: str = Query(...,description="Text to search in title or content"),
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
    
):
    notes = (
        db.query(AppNotes)
        .filter(
            AppNotes.user_id == current_user.id,
            (AppNotes.title.ilike(f"%{q}%") | AppNotes.content.ilike(f"%{q}%"))
        ).all()
    )
    return notes


