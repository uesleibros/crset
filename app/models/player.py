from pydantic import BaseModel
from typing import List, Optional

class Rating(BaseModel):
    base: int
    delta: Optional[int] = 0

class PlayerSummary(BaseModel):
    id: int
    name: str
    overall: Rating
    potential: Rating
    age: int
    nationality: str
    club: str
    positions: List[str]
    value: str
    wage: str
    total_stats: int

class PaginatedPlayers(BaseModel):
    page: int
    count: int
    has_next: bool
    results: List[PlayerSummary]