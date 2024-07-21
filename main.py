from typing import Dict, List, Optional, Union
import csv
from scraping.scraper import MateTeeScraper


def write_to_csv(
    data: List[Dict[str, Optional[Union[str, bool, List[str]]]]], filename: str
) -> None:
    fieldnames = [
        "brand_name",
        "country_of_origin",
        "product_title",
        "contains_stems",
        "flavor_intensity",
        "yerba_mate_type",
        "is_smoked",
        "is_organic",
        "product_descriptions",
    ]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    base_url = "https://www.mate-tee.de/en/Yerba-Mate-by-Country:::6.html?offset=9999&trigger=scroll&sort=default&category=6"
    scraper = MateTeeScraper(base_url)
    links = scraper.fetch_links()
    data = scraper.scrape(links)
    write_to_csv(data, "test.csv")
