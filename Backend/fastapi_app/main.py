from fastapi import FastAPI
from .notes_endpoint import notes_router as notes_router
from .tags_endpoint import tags_router as tags_router
app = FastAPI()
app.include_router(notes_router)
app.include_router(tags_router)