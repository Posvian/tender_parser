import argparse
from parser import parse_tenders
from storage import save_to_csv, save_to_sqlite


def main():
    """
    Основная функция для парсинга и сохранения тендеров с сайта rostender.
    """
    parser = argparse.ArgumentParser(description="Парсер тендеров с rostender")
    parser.add_argument(
        "--max", type=int, default=100, help="Необходимое количество тендеров"
    )
    parser.add_argument(
        "--output", type=str, help="Файл для сохранения (CSV или SQLite)"
    )

    args = parser.parse_args()

    tenders = parse_tenders(args.max)

    if args.output:
        if args.output.endswith(".csv"):
            save_to_csv(tenders=tenders, filename=args.output)
        elif args.output.endswith(".db") or args.output.endswith(".sqlite"):
            save_to_sqlite(tenders=tenders, dbname=args.output)
        else:
            print("Неподдерживаемый формат файла. Используйте .csv или .db/.sqlite")
    else:
        for tender in tenders:
            print(f"{tender['tender_number']}: {tender['tender_title']}")


if __name__ == "__main__":
    main()
