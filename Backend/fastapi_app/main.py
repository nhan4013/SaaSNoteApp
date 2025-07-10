from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppNotes, AuthUser
from .schemas import NoteOut
from .dependencies import get_current_user

app = FastAPI()


@app.get("/notes/", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == current_user.id).all()
    return notes




