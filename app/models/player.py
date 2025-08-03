"""
Data models for player-related responses used in the CRSet API.
"""

from typing import List, Optional

from pydantic import BaseModel


class Rating(BaseModel):
    """
    Represents a player's rating with a base value and an optional delta.
    """

    base: int
    delta: Optional[int] = 0


class PlayerSummary(BaseModel):
    """
    Represents summarized information about a football player.
    """

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
    """
    Represents a paginated response containing a list of players.
    """

    page: int
    count: int
    has_next: bool
    results: List[PlayerSummary]
