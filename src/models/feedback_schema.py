from pydantic import BaseModel
from typing import List


class MemoryBlock(BaseModel):
    id: str
    text: str
    event: str


class AllBlocks(BaseModel):
    memory: List[MemoryBlock]
