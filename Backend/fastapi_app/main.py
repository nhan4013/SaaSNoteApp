from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import AppNotes, AuthUser
from .schemas import NoteOut, NoteIn
from .dependencies import get_current_user
from fastapi import status,HTTPException
from datetime import datetime,timezone

app = FastAPI()

#GET /notes/ — List all notes of the current user
@app.get("/notes/", response_model=list[NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    # Query notes that belong to the current user
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == current_user.id).all()

    return notes

 # Get the note by ID and check if it belongs to the user
@app.get("/notes/{id}", response_model=NoteOut)
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
    note.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(note)
    return note

# DELETE /notes/{id} — Delete a note
@app.delete("/notes/{id}",status_code=status.HTTP_200_OK)
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

#  POST /notes/ — Create a new note
@app.post("/notes/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteIn, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    new_note = AppNotes(
        title=note.title, content=note.content, user_id=current_user.id, created_at=now,
        updated_at=now)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
