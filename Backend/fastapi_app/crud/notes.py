from datetime import datetime, timezone
from fastapi import HTTPException
from utils.transition import note_to_schema
from models import AppNotes, AppNotesTags, AppTags
from utils.redis_pubsub import publish_update


async def after_note_change(db, user):
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == user.id).all()
    notes_data = [note_to_schema(note) for note in notes]
    json_data = "[" + ",".join([note.model_dump_json() for note in notes_data]) + "]"
    await publish_update("notes",json_data)

async def get_notes(db, user):
    notes = db.query(AppNotes).filter(
        AppNotes.user_id == user.id).all()
    return [note_to_schema(note) for note in notes]


async def get_note_id(id, db, user):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_to_schema(note)


async def update_note(id, note_in, db, user):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_in.title
    note.content = note_in.content
    note.updated_at = datetime.now(timezone.utc)
    note.is_archived = getattr(note_in, "is_archived", note.is_archived) 
    note.app_notes_tags.clear()
    db.commit()
    for tag_name in note_in.tags:
        tag = db.query(AppTags).filter_by(
            name=tag_name, user_id=user.id).first()
        if not tag:
            tag = AppTags(name=tag_name, user_id=user.id)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        note.app_notes_tags.append(tag)
    db.commit()
    db.refresh(note)
    await after_note_change(db,user)
    return note_to_schema(note)


async def delete_note(id, db, user):
    note = db.query(AppNotes).filter(
        AppNotes.id == id,
        AppNotes.user_id == user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    await after_note_change(db,user)
    return {"message": f"Note {id} deleted successfully"}


async def create_node(note_in, db, user):
    now = datetime.now(timezone.utc)
    new_note = AppNotes(
        title=note_in.title, content=note_in.content, user_id=user.id, created_at=now,
        updated_at=now,is_archived = False)
    for tag_name in note_in.tags:
        tag = db.query(AppTags).filter_by(
            name=tag_name, user_id=user.id).first()
        if not tag:
            tag = AppTags(name=tag_name, user_id=user.id)
            db.add(tag)
            db.flush()
        link = AppNotesTags(notes=new_note, tags=tag)
        new_note.app_notes_tags.append(link)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    print("Publishing notes update")
    await after_note_change(db,user)
    return note_to_schema(new_note)


def search_notes_by_tag(tag, q, db, user):
    query = db.query(AppNotes).filter(AppNotes.user_id == user.id)
    if tag:
        query = query.join(AppNotes.app_notes_tags).filter(AppTags.name == tag)
    if q:
        query = query.filter((AppNotes.title.ilike(
            f"%{q}%") | AppNotes.content.ilike(f"%{q}%")))
    notes = query.all()
    return [note_to_schema(note) for note in notes]
