import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union
from .fetcher import MateTeeLinkFetcher, WebDriverSetup
from .extractor import MateTeeExtractor
from .parser import MateTeeParser


class MateTeeScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = WebDriverSetup.setup_driver()

    def fetch_links(self) -> List[str]:
        link_fetcher = MateTeeLinkFetcher(self.driver)
        links = link_fetcher.fetch_links(self.base_url)
        self.driver.quit()
        return links

    def scrape(
        self, urls: Union[str, List[str]]
    ) -> Union[
        Dict[str, Optional[Union[str, bool, List[str]]]],
        List[Dict[str, Optional[Union[str, bool, List[str]]]]],
    ]:
        if isinstance(urls, str):
            return self._scrape_single(urls)
        elif isinstance(urls, list):
            return [self._scrape_single(url) for url in urls]

    def _scrape_single(
        self, url: str
    ) -> Dict[str, Optional[Union[str, bool, List[str]]]]:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        extractor = MateTeeExtractor()
        parser = MateTeeParser(extractor)
        return parser.parse_page(soup)
