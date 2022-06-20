import pickle
import re
from pathlib import Path
from typing import List, Optional

import arxivscraper

DATA_DIR = Path("./data")


def _remove_double_spaces(s: str) -> str:
    return re.sub("\s+", " ", s)


def get_ml_titles_from_cat(
    cat: str,
    subcat: Optional[str] = None,
    date_from: Optional[str] = None,
    date_until: Optional[str] = None,
) -> List[str]:

    filters = {"categories": [f"{cat}.{subcat}"]} if subcat else {}

    scraper = arxivscraper.Scraper(
        category=cat,
        date_from=date_from,
        date_until=date_until,
        filters=filters,
    )
    cslg_outputs = scraper.scrape()

    cslg_titles_and_urls = {
        (_remove_double_spaces(record.get("title", None)), record.get("url", None))
        for record in cslg_outputs
    }

    return cslg_titles_and_urls


def get_and_save_info(date_from, date_to):

    filename = DATA_DIR / f"stat-ml_cs-LG_{date_from}-{date_to}.pkl"

    all_titles_and_urls = get_ml_titles_from_cat("stat", "ML", date_from).union(
        get_ml_titles_from_cat("cs", "LG", date_to)
    )

    with open(filename, "wb") as f:
        pickle.dump(all_titles_and_urls, f)

    return all_titles_and_urls
