import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


BASE_URL = "https://rostender.info"


def parse_tenders(max_count: int = 100) -> list[dict]:
    tenders = []
    page = 1
    while len(tenders) < max_count:
        url = f"{BASE_URL}/extsearch?page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            tender_articles = soup.select("article.tender-row")

            if not tender_articles:
                break

            for article in tender_articles[: max_count - len(tenders)]:
                try:
                    tender_number = article.get("id", "")

                    element_title = article.select_one(".tender-info__description")
                    tender_title = (
                        element_title.get_text(strip=True) if element_title else ""
                    )
                    tender_link = (
                        urljoin(BASE_URL, element_title["href"])
                        if element_title
                        else ""
                    )

                    element_start_date = article.select_one(".tender__date-start")
                    tender_start_date = (
                        element_start_date.get_text(strip=True)
                        .replace("от", "")
                        .strip()
                        if element_start_date
                        else ""
                    )

                    element_end_date = article.select_one(".tender__countdown-text")
                    tender_date_end = ""
                    tender_time_end = ""
                    if element_end_date:
                        element_date_text = element_end_date.get_text(strip=True)
                        date_match = re.search(
                            r"(\d{2}\.\d{2}\.\d{4})", element_date_text
                        )
                        time_match = re.search(r"(\d{2}:\d{2})", element_date_text)
                        if date_match:
                            tender_date_end = date_match.group(1)
                        if time_match:
                            tender_time_end = time_match.group(1)

                    element_region = article.select_one(".tender-address .line-clamp")
                    tender_region = (
                        element_region.get_text(strip=True) if element_region else ""
                    )

                    element_price = article.select_one(".starting-price__price")
                    tender_price = (
                        element_price.get_text(strip=True) if element_price else ""
                    )

                    categories = []
                    element_category = article.select(".list-branches__link")
                    for category in element_category:
                        categories.append(category.get_text(strip=True))

                    tender = {
                        "tender_number": tender_number,
                        "tender_title": tender_title,
                        "tender_link": tender_link,
                        "tender_start_date": tender_start_date,
                        "tender_date_end": tender_date_end,
                        "tender_time_end": tender_time_end,
                        "tender_region": tender_region,
                        "tender_price": tender_price,
                        "categories": ", ".join(categories),
                    }
                    tenders.append(tender)

                except Exception as e:
                    print(f"Ошибка при парсинге карточки тендера: {e}")
                    continue

            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе страницы {page}: {e}")
            break

    return tenders[:max_count]


if __name__ == "__main__":
    print(parse_tenders())
