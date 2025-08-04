"""
Module responsible for scraping the player list from a given URL.
"""

from typing import List, Optional

import curl_cffi
from selectolax.parser import HTMLParser

from app.models.player import PlayerSummary
from app.utils.headers import HEADERS
from app.utils.parsers import parse_rating


# pylint: disable=too-many-locals
def parse_player_row(row) -> Optional[PlayerSummary]:
	"""
	Parses a single HTML row element and extracts player data.

	Args:
		row: HTML element representing a table row.

	Returns:
		PlayerSummary object if parsing is successful, None otherwise.
	"""

	age_col = row.css_first('td[data-col="ae"]')          # Age
	overall_col = row.css_first('td[data-col="oa"]')      # Overall rating  
	potential_col = row.css_first('td[data-col="pt"]')    # Potential
	value_col = row.css_first('td[data-col="vl"]')        # Value
	wage_col = row.css_first('td[data-col="wg"]')         # Wage
	total_stats_col = row.css_first('td[data-col="tt"]')  # Total stats

	cols = row.css("td")
	if len(cols) < 10:
		return None

	name_col = cols[1]
	club_col = cols[5]

	if not all([name_col, age_col, overall_col, potential_col]):
		return None

	link = name_col.css_first("a")
	if not link:
		return None

	href = link.attributes.get("href", "")
	try:
		player_id = int(href.split("/")[2])
	except (IndexError, ValueError):
		return None

	name = link.text().strip()
	age = int(age_col.text().strip())
	overall_em = overall_col.css_first("em")
	if overall_em and overall_em.attributes.get("title"):
		overall = parse_rating(overall_em.attributes.get("title"))
	else:
		overall = parse_rating(overall_col.text())
	
	potential_em = potential_col.css_first("em") 
	if potential_em and potential_em.attributes.get("title"):
		potential = parse_rating(potential_em.attributes.get("title"))
	else:
		potential = parse_rating(potential_col.text())
	
	nat_img = name_col.css_first("img.flag")
	nationality = nat_img.attributes.get("title", "").strip() if nat_img else ""
	
	club_link = club_col.css_first("a")
	club = club_link.text().strip() if club_link else ""
	
	value = value_col.text().strip() if value_col else ""
	wage = wage_col.text().strip() if wage_col else ""
	total_stats = int(total_stats_col.text().strip()) if total_stats_col else 0
	positions = [span.text().strip() for span in cols[1].css("span.pos")]

	return PlayerSummary(
		id=player_id,
		name=name,
		overall=overall,
		potential=potential,
		age=age,
		nationality=nationality,
		club=club,
		positions=positions,
		value=value,
		wage=wage,
		total_stats=total_stats,
	)


async def scrape_player_list(url: str) -> List[PlayerSummary]:
	"""
	Asynchronously fetches the player list page and parses player data.

	Args:
		url: URL of the player list page.

	Returns:
		List of PlayerSummary objects.
	"""
	async with curl_cffi.AsyncSession(headers=HEADERS, impersonate="chrome") as session:
		response = await session.get(url)
		response.raise_for_status()
		html = response.text

	tree = HTMLParser(html)
	players: List[PlayerSummary] = []

	for row in tree.css("table tbody tr"):
		player = parse_player_row(row)
		if player:
			players.append(player)

	return players
