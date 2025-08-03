CREATE_TABLE_TENDERS = """CREATE TABLE IF NOT EXISTS tenders
                 (tender_number text, tender_title text, tender_link text, tender_start_date text, tender_date_end text, tender_price text, tender_region text)"""

INSERT_VALUES = "INSERT INTO tenders VALUES (?, ?, ?, ?, ?, ?, ?)"
