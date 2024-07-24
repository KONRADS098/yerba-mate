from typing import Dict, List, Optional, Union
from bs4 import BeautifulSoup
from .extractor import MateTeeExtractor


class MateTeeParser:
    def __init__(self, extractor: MateTeeExtractor):
        self.extractor = extractor

    def parse_page(
        self, soup: BeautifulSoup
    ) -> Dict[str, Optional[Union[str, bool, List[str]]]]:
        subtitle_data = self.extractor.extract_subtitle(soup)
        product_data = {
            "brand_name": self.extractor.extract_brand_name(soup),
            "country_of_origin": self.extractor.extract_country_of_origin(soup),
            "product_title": self.extractor.extract_product_title(soup),
            "contains_stems": subtitle_data.get("contains_stems"),
            "flavor_intensity": subtitle_data.get("flavor_intensity"),
            "yerba_mate_type": subtitle_data.get("yerba_mate_type"),
            "is_smoked": subtitle_data.get("is_smoked"),
            "is_organic": subtitle_data.get("is_organic"),
            "product_descriptions": subtitle_data.get("tags", [])
            + (self.extractor.extract_keywords(soup) or []),
        }
        return product_data
