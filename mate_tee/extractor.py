from typing import Dict, List, Optional, Union
from bs4 import BeautifulSoup


class MateTeeExtractor:
    @staticmethod
    def extract_brand_name(soup: BeautifulSoup) -> Optional[str]:
        try:
            label = soup.find(string="Brand:")
            label_parent = label.find_parent("div")
            container = label_parent.find_parent("div")
            columns = container.find_all("div", recursive=False)
            value_column = (
                columns[1] if columns.index(label_parent) == 0 else columns[0]
            )
            brand_link = value_column.find("a")
            return brand_link.text.strip() if brand_link else None
        except AttributeError:
            return None

    @staticmethod
    def extract_country_of_origin(soup: BeautifulSoup) -> Optional[str]:
        try:
            label = soup.find("strong", string="Origin")
            label_parent = label.find_parent("p")
            return label_parent.text.strip().split(":")[-1].strip()
        except AttributeError:
            return None

    @staticmethod
    def extract_product_title(soup: BeautifulSoup) -> Optional[str]:
        product_title_section = soup.find("h1", class_="h3", itemprop="name")
        return product_title_section.text.strip() if product_title_section else None

    @staticmethod
    def extract_subtitle(soup: BeautifulSoup) -> Dict[str, Union[str, bool, List[str]]]:
        try:
            subtitle_section = soup.find("small", class_="attributeDoofinder")
            subtitle = subtitle_section.text.strip()
            parts = [part.strip() for part in subtitle.split(">")]
            info = {
                "contains_stems": "with stems" in subtitle.lower(),
                "flavor_intensity": next(
                    (
                        part.split(" ")[-1].capitalize()
                        for part in parts
                        if any(
                            intensity in part.lower()
                            for intensity in ["mild", "medium", "strong"]
                        )
                    ),
                    None,
                ),
                "yerba_mate_type": next(
                    (
                        part
                        for part in parts
                        if any(
                            type_ in part.lower()
                            for type_ in [
                                "pure mate",
                                "with other herbs",
                                "mixed with fruits",
                            ]
                        )
                    ),
                    None,
                ),
                "is_smoked": "smoked" in subtitle.lower(),
                "is_organic": "organic" in subtitle.lower(),
                "tags": [
                    part
                    for part in parts
                    if part
                    and not any(
                        keyword in part.lower()
                        for keyword in [
                            "with stems",
                            "mild",
                            "medium",
                            "strong",
                            "pure mate",
                            "with other herbs",
                            "mixed with fruits",
                            "smoked",
                            "organic",
                        ]
                    )
                ],
            }
            return info
        except AttributeError:
            return {
                "contains_stems": False,
                "flavor_intensity": None,
                "yerba_mate_type": None,
                "is_smoked": False,
                "is_organic": False,
                "tags": [],
            }

    @staticmethod
    def extract_keywords(soup: BeautifulSoup) -> Optional[List[str]]:
        try:
            hidden_input = soup.find("input", attrs={"name": "about-display"})
            parent = hidden_input.find_parent("div", class_="product-section")
            description = parent.find("section")
            return (
                [strong.text for strong in description.find_all("strong")]
                if description
                else None
            )
        except AttributeError:
            return None
