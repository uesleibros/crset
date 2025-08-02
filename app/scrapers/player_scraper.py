import curl_cffi
import re
from selectolax.parser import HTMLParser
from typing import List
from app.models.player import PlayerSummary, Rating

HEADERS = {
	"Authority": "sofifa.com",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
	"Cache-Control": "max-age=0",
	"Referer": "https://sofifa.com/",
	"Priority": "u=0, i",
	"Sec-CH-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
	"Sec-CH-Ua-Mobile": "?0",
	"Sec-CH-Ua-Platform": '"Windows"',
	"Sec-Fetch-Dest": "document",
	"Sec-Fetch-Mode": "navigate",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-User": "?1",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def parse_rating(raw: str) -> Rating:
	base_match = re.match(r"\d+", raw.strip())
	delta_match = re.search(r"([+-]\d+)", raw.strip())

	base = int(base_match.group()) if base_match else 0
	delta = int(delta_match.group()) if delta_match else 0

	return Rating(base=base, delta=delta)

async def scrape_player_list(url: str) -> List[PlayerSummary]:
	async with curl_cffi.AsyncSession(headers=HEADERS, impersonate="chrome") as session:
		response = await session.get(url)
		response.raise_for_status()
		html = response.text

	tree = HTMLParser(html)
	players: List[PlayerSummary] = []

	for row in tree.css("table tbody tr"):
		cols = row.css("td")
		if len(cols) < 10:
			continue

		link = cols[1].css_first("a")
		if not link:
			continue

		href = link.attributes.get("href", "")
		try:
			player_id = int(href.split("/")[2])
		except (IndexError, ValueError):
			continue

		name = link.text().strip()
		age = int(cols[2].text().strip())
		overall = parse_rating(cols[3].text())
		potential = parse_rating(cols[4].text())

		nat_img = cols[1].css_first("img.flag")
		nationality = nat_img.attributes.get("title", "").strip() if nat_img else ""

		club_link = cols[5].css_first("a")
		club = club_link.text().strip() if club_link else ""

		value = cols[6].text().strip()
		wage = cols[7].text().strip()
		total_stats = int(cols[8].text().strip())
		positions = [span.text().strip() for span in cols[1].css("span.pos")]

		players.append(
			PlayerSummary(
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
				total_stats=total_stats
			)
		)

	return players