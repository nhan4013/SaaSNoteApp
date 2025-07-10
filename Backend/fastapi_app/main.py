from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppNotes, AuthUser
from .schemas import NoteOut, NoteIn
from .dependencies import get_current_user
from fastapi import status
from datetime import datetime

app = FastAPI()


@app.get("/notes/", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == current_user.id).all()
    result = []
    
    return notes

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
