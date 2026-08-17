# Pull data from OpenF1 into raw tables.
#
#   python fetch.py --endpoint sessions --year 2024 --dry-run
#   python fetch.py --endpoint laps --session 9158
#   python fetch.py --endpoint laps --session 9158 --to-csv snapshot/laps.csv
#
# What this already does: calls the API, shows you what came back, and appends it to
# a table called raw_<endpoint>.
#
# What it does not do, and you need to:
#   - decide what to pull, and how much of it
#   - make it safe to run twice (see the TODO in load())
#   - fail loudly and usefully when the API misbehaves
#
# Check the endpoint names and filters against the documentation at openf1.org. They
# are not guaranteed to match what is written here.

import argparse
import os
import sys

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_URL = "https://api.openf1.org/v1"


def fetch(endpoint: str, params: dict) -> list:
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        sys.exit(f"expected a list from {url}, got {type(payload).__name__}")
    return payload


def load(frame: pd.DataFrame, table: str, database_url: str) -> None:
    engine = create_engine(database_url)

    # TODO make this safe to run twice.
    #
    # if_exists="append" does exactly what it says: run this command again and every
    # row is inserted again. Reload one session twice and your counts double, which
    # is the kind of error that does not throw and does not show up until a chart
    # looks slightly wrong.
    #
    # Look up primary keys and INSERT ... ON CONFLICT. You will need a real key
    # first: work out which columns actually identify one row, and if none of them
    # do, build one and write that decision into AGREEMENT.md.
    frame.to_sql(table, engine, if_exists="append", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull OpenF1 data into raw tables.")
    parser.add_argument("--endpoint", required=True,
                        help="OpenF1 endpoint, e.g. sessions, drivers, laps, stints, pit, weather")
    parser.add_argument("--session", type=int, help="filter by session_key")
    parser.add_argument("--year", type=int, help="filter by year")
    parser.add_argument("--driver", type=int, help="filter by driver_number")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what came back and write nothing")
    parser.add_argument("--to-csv", metavar="PATH",
                        help="write to a CSV instead of the database")
    args = parser.parse_args()

    load_dotenv()

    params = {}
    if args.session:
        params["session_key"] = args.session
    if args.year:
        params["year"] = args.year
    if args.driver:
        params["driver_number"] = args.driver

    rows = fetch(args.endpoint, params)
    print(f"{len(rows)} rows from /{args.endpoint} {params or ''}")

    if not rows:
        print("nothing came back. Check your filters against the docs.")
        return

    frame = pd.DataFrame(rows)

    print()
    print(frame.head(5).to_string())
    print()
    print("columns and types as they arrived:")
    print(frame.dtypes.to_string())
    print()
    print("Look at the columns above and ask: which of these repeat something you")
    print("already know from another endpoint? That repetition is your normalisation")
    print("exercise, and it is easier to see now than tomorrow.")

    if args.to_csv:
        os.makedirs(os.path.dirname(args.to_csv) or ".", exist_ok=True)
        frame.to_csv(args.to_csv, index=False)
        print(f"\nwrote {args.to_csv}")
        return

    if args.dry_run:
        print("\ndry run - nothing written")
        return

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        sys.exit("DATABASE_URL is not set. Copy .env.example to .env and fill it in.")

    table = f"raw_{args.endpoint}"
    load(frame, table, database_url)
    print(f"\nappended {len(frame)} rows to {table}")


if __name__ == "__main__":
    main()
