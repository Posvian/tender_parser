import csv
import sqlite3

from queries import CREATE_TABLE_TENDERS, INSERT_VALUES


def save_to_csv(tenders: list[dict], filename: str):
    """Сохраняет список тендеров в CSV файл."""
    if not tenders:
        return

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = tenders[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tenders)


def save_to_sqlite(tenders: list[dict], dbname: str = "tenders.db"):
    """Сохраняет список тендеров в SQLite базу данных"""
    if not tenders:
        return

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute(CREATE_TABLE_TENDERS)

    for tender in tenders:
        cursor.execute(
            INSERT_VALUES,
            (
                tender["tender_number"],
                tender["tender_title"],
                tender["tender_link"],
                tender["tender_start_date"],
                tender["tender_date_end"],
                tender["tender_price"],
                tender["tender_region"],
            ),
        )
    conn.commit()
    conn.close()
