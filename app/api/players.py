"""Player list endpoints with pagination for various SoFIFA filters."""

from fastapi import APIRouter, Query

from app.models.player import PaginatedPlayers
from app.scrapers.player_list_scraper import scrape_player_list

router = APIRouter()


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
