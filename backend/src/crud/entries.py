from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Entries
from src.schemas.entries import EntryOutSchema
from src.schemas.token import Status


async def get_entries():
    return await EntryOutSchema.from_queryset(Entries.all())


async def get_entry(entry_id) -> EntryOutSchema:
    return await EntryOutSchema.from_queryset_single(Entries.get(id=entry_id))


async def create_entry(entry, current_user) -> EntryOutSchema:
    entry_dict = entry.dict(exclude_unset=True)
    entry_dict["author_id"] = current_user.id
    entry_obj = await Entries.create(**entry_dict)
    return await EntryOutSchema.from_tortoise_orm(entry_obj)


async def update_entry(entry_id, entry, current_user) -> EntryOutSchema:
    try:
        db_entry = await EntryOutSchema.from_queryset_single(Entries.get(id=entry_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")

    if db_entry.author.id == current_user.id:
        await Entries.filter(id=entry_id).update(**entry.dict(exclude_unset=True))
        return await EntryOutSchema.from_queryset_single(Entries.get(id=entry_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_entry(entry_id, current_user) -> Status:
    try:
        db_entry = await EntryOutSchema.from_queryset_single(Entries.get(id=entry_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")

    if db_entry.author.id == current_user.id:
        deleted_count = await Entries.filter(id=entry_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")
        return Status(message=f"Deleted entry {entry_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
