from schemas import NoteOut
from models import AppNotes

def note_to_schema(note: AppNotes) -> NoteOut:
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
        user_id=note.user_id,
        is_archived=note.is_archived,
        tags=[tag.tags.name for tag in note.app_notes_tags]
    )