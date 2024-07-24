import csv
from typing import Dict, List, Optional, Union


def write_to_csv(
    data: List[Dict[str, Optional[Union[str, bool, List[str]]]]],
    filename: str,
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
