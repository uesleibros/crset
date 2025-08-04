"""Player list endpoints with pagination for various SoFIFA filters."""

from fastapi import APIRouter, Query

from app.models.player import PaginatedPlayers
from app.utils.maps import COUNTRY_MAP, PREFERRED_FOOT
from app.scrapers.player_list_scraper import scrape_player_list

from typing import Optional, List

from enum import Enum

router = APIRouter()

class Foot(str, Enum):
	left = "left"
	right = "right"

def create_country_enum():
    return Enum(
        'Country',
        {key.lower(): key.title() for key in COUNTRY_MAP}
    )

CountryEnum = create_country_enum()

def build_url(base: str, page: int) -> str:
	"""Constructs the full URL with the correct offset for pagination."""
	offset = max(page - 1, 0) * 60
	if offset > 0:
		return f"{base}&offset={offset}" if "?" in base else f"{base}?offset={offset}"
	return base


async def paginated_response(base_url: str, page: int) -> PaginatedPlayers:
	"""Returns a paginated response based on the provided base URL and page."""
	players = await scrape_player_list(build_url(base_url, page))
	return PaginatedPlayers(
		page=page,
		count=len(players),
		has_next=len(players) == 60,
		results=players,
	)

@router.get("/search", response_model=PaginatedPlayers)
async def search_players(
	page: int = Query(1, ge=1), 
	keyword: Optional[str] = Query(None, description="Search by player name"),
	nationality: Optional[List[CountryEnum]] = Query(None, description="Filter by nationality (e.g., Brazil, Argentina)"),
	league: Optional[str] = Query(None, description="Filter by league (e.g., La Liga, Premier League)"),
	preferred_foot: Optional[List[Foot]] = Query(
		None, 
		alias="preferred_foot", 
		description="Preferred Foot: Right, Left."
	),
	club: Optional[str] = Query(None, description="Filter by club/team"),
	type_filter: Optional[str] = Query(
		None,
		description="Type of player: all, added, updated, free, onLoan, removed, customized, history",
		regex="^(all|added|updated|free|onLoan|removed|customized|history)$"
	)
):
	"""
	Search players on SOFIFA with pagination and filters.
	"""
	base_url = "https://sofifa.com/players"
	params = {}

	if keyword:
		params["keyword"] = keyword
	if preferred_foot:
		for pf in preferred_foot:
			params.setdefault("pf[]", []).append(PREFERRED_FOOT.get(pf))
	if type_filter:
		params["type"] = type_filter
	if nationality:
		for na in nationality:
			params.setdefault("na[]", []).append(COUNTRY_MAP.get(na.value.lower()))
	
	query_parts = []
	for key, value in params.items():
		if isinstance(value, list):
			query_parts.extend(f"{key}={v}" for v in value)
		else:
			query_parts.append(f"{key}={value}")

	query_string = "&".join(query_parts)
	url = f"{base_url}?{query_string}" if query_string else base_url

	print(f"Requesting SOFIFA URL: {url}")
	return await paginated_response(url, page)

@router.get("/trending", response_model=PaginatedPlayers)
async def get_trending_players(page: int = Query(1, ge=1)):
	"""Get players from trending list."""
	return await paginated_response("https://sofifa.com/players", page)


@router.get("/added", response_model=PaginatedPlayers)
async def get_recently_added(page: int = Query(1, ge=1)):
	"""Get recently added players."""
	return await paginated_response("https://sofifa.com/players?type=added", page)


@router.get("/updated", response_model=PaginatedPlayers)
async def get_recently_updated(page: int = Query(1, ge=1)):
	"""Get recently updated players."""
	return await paginated_response("https://sofifa.com/players?type=updated", page)


@router.get("/free", response_model=PaginatedPlayers)
async def get_free_agents(page: int = Query(1, ge=1)):
	"""Get free agent players."""
	return await paginated_response("https://sofifa.com/players?type=free", page)


@router.get("/onLoan", response_model=PaginatedPlayers)
async def get_on_loan_players(page: int = Query(1, ge=1)):
	"""Get players currently on loan."""
	return await paginated_response("https://sofifa.com/players?type=onLoan", page)


@router.get("/removed", response_model=PaginatedPlayers)
async def get_removed_players(page: int = Query(1, ge=1)):
	"""Get players recently removed."""
	return await paginated_response("https://sofifa.com/players?type=removed", page)


@router.get("/customized", response_model=PaginatedPlayers)
async def get_customized_players(page: int = Query(1, ge=1)):
	"""Get customized players."""
	return await paginated_response("https://sofifa.com/players?type=customized", page)
