from .scraper import MateTeeScraper
from .writer import write_to_csv


def main():
    base_url = "https://www.mate-tee.de/en/Yerba-Mate-by-Country:::6.html?offset=9999&trigger=scroll&sort=default&category=6"
    scraper = MateTeeScraper(base_url)
    links = scraper.fetch_links()
    data = scraper.scrape(links)
    write_to_csv(data, "test.csv")
