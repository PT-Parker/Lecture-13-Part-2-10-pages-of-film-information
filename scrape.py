"""
Fetch movie listing pages from https://ssr1.scrape.center/page/1..10,
save the HTML locally, and extract movie data to a CSV file.
"""
from pathlib import Path
import csv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


BASE_URL = "https://ssr1.scrape.center"
OUTPUT_DIR = Path(".")
CSV_FILE = OUTPUT_DIR / "movies.csv"
PAGE_COUNT = 10


def create_session(verify: bool = True) -> requests.Session:
    """Create a session with retry and a default UA; allow toggling SSL verify."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MovieScraper/1.0"}
    )
    session.verify = verify
    return session


def fetch_page(page: int, session: requests.Session) -> str:
    url = f"{BASE_URL}/page/{page}"
    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    html = resp.text
    (OUTPUT_DIR / f"page{page}.html").write_text(html, encoding="utf-8")
    return html


def parse_movies(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    movies = []
    for card in soup.select("div.el-card"):
        title_el = card.select_one("a.name h2")
        score_el = card.select_one("p.score")
        categories = [span.get_text(strip=True) for span in card.select(".categories span")]
        info_blocks = card.select("div.m-v-sm.info")

        region = ""
        runtime = ""
        release_date = ""
        if info_blocks:
            spans = [span.get_text(strip=True) for span in info_blocks[0].find_all("span")]
            if spans:
                region = spans[0]
            if len(spans) >= 3:
                runtime = spans[2]
        if len(info_blocks) >= 2:
            release_date = info_blocks[1].get_text(strip=True)

        movies.append(
            {
                "Title": title_el.get_text(strip=True) if title_el else "",
                "Score": score_el.get_text(strip=True) if score_el else "",
                "Categories": "|".join(categories),
                "Region": region,
                "Runtime": runtime,
                "ReleaseDate": release_date,
            }
        )
    return movies


def save_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = ["Title", "Score", "Categories", "Region", "Runtime", "ReleaseDate"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    all_movies: list[dict] = []
    session = create_session(verify=True)
    insecure_session = None

    for page in range(1, PAGE_COUNT + 1):
        try:
            html = fetch_page(page, session=session)
        except requests.exceptions.SSLError:
            # Fallback with verify=False if SSL handshake fails.
            if insecure_session is None:
                insecure_session = create_session(verify=False)
            html = fetch_page(page, session=insecure_session)
        all_movies.extend(parse_movies(html))
    save_csv(all_movies, CSV_FILE)


if __name__ == "__main__":
    main()
