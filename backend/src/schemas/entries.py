from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Entries


EntryInSchema = pydantic_model_creator(
    Entries,
    name="EntryIn",
    exclude=["author_id"],
    exclude_readonly=True,
)
EntryOutSchema = pydantic_model_creator(
    Entries,
    name="Entry",
    exclude=[
        "author.password",
        "author.created_at",
        "author.modified_at",
        "author.note",
    ],
)


class UpdateEntry(BaseModel):
    setup: Optional[str]
    order: Optional[str]
    result: Optional[float]
    obs: Optional[str]
