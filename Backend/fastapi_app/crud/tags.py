from fastapi import HTTPException
from models import AppTags
from utils.redis_pubsub import publish_update
import json

async def after_tag_change(db, user):
    tags = db.query(AppTags).filter(AppTags.user_id == user.id).all()
    await publish_update("tags",json.dumps(tags))


async def list_tags(db, user):
    tags = db.query(AppTags).filter(AppTags.user_id == user.id).all()
    return tags


async def create_tag(tag_in, db, user):
    new_tag = AppTags(name=tag_in.name, user_id=user.id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    await after_tag_change(db,user)
    return new_tag


async def update_tag(id, tag_in, db, user):
    tag_update = db.query(AppTags).filter(
        AppTags.id == id,
        AppTags.user_id == user.id
    ).first()
    if not tag_update:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_update.name = tag_in.name
    db.commit()
    db.refresh(tag_update)
    await after_tag_change(db,user)
    return tag_update
