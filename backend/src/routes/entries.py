from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.entries as crud
from src.auth.jwthandler import get_current_user
from src.schemas.entries import EntryOutSchema, EntryInSchema, UpdateEntry
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/entries",
    response_model=List[EntryOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_entries():
    return await crud.get_entries()


@router.get(
    "/entry/{entry_id}",
    response_model=EntryOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_entry(entry_id: int) -> EntryOutSchema:
    try:
        return await crud.get_entry(entry_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Entry does not exist",
        )


@router.post(
    "/entries",
    response_model=EntryOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def create_entry(
    entry: EntryInSchema,
    current_user: UserOutSchema = Depends(get_current_user),
) -> EntryOutSchema:
    return await crud.create_entry(entry, current_user)


@router.patch(
    "/entry/{entry_id}",
    dependencies=[Depends(get_current_user)],
    response_model=EntryOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_entry(
    entry_id: int,
    entry: UpdateEntry,
    current_user: UserOutSchema = Depends(get_current_user),
) -> EntryOutSchema:
    return await crud.update_entry(entry_id, entry, current_user)


@router.delete(
    "/entry/{entry_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_entry(
    entry_id: int,
    current_user: UserOutSchema = Depends(get_current_user),
):
    return await crud.delete_entry(entry_id, current_user)
