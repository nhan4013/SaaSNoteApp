from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppNotes, AuthUser
from .schemas import NoteOut, NoteIn
from .dependencies import get_current_user
from fastapi import status,HTTPException
from datetime import datetime

app = FastAPI()


@app.get("/notes/", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == current_user.id).all()

    return notes


@app.get("/notes/{id})", response_model=NoteOut)
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

@app.put("/notes/{id}",response_model=NoteOut)
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
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{id}",status_code=status.HTTP_204_NO_CONTENT)
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
    return {"message": f"Note {id} deleted"}


@app.post("/notes/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteIn, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    now = datetime.utcnow()
    new_note = AppNotes(
        title=note.title, content=note.content, user_id=current_user.id, created_at=now,
        updated_at=now)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
