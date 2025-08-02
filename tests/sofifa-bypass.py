import curl_cffi

URL: str = "https://sofifa.com/players"
HEADERS: dict = {
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
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

print(curl_cffi.get(URL, headers=HEADERS, impersonate="chrome").status_code)