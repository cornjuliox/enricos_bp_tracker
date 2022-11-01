# NOTE: This is a one-shot script that I used to convert an existing csv spreadsheet with BP data
#       into a json file suitable for use with the main program.
# NOTE: If you didn't understand any of that you can safely ignore this file.
import argparse
import pathlib
import json
import datetime
from typing import Optional
from datetime import timezone, tzinfo
from csv import DictReader

import arrow

SYSTZ: Optional[tzinfo] = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str, help="Path to the input tsv file.")
parser.add_argument("outpath", type=str, help="Path to the desired output location.")
parser.add_argument("--console_only", action="store_true", default=False)
cli_args: argparse.Namespace = parser.parse_args()

def __clean_dict(dict_in: dict) -> dict:
    copy: dict = {x.lower(): y for (x, y) in dict_in.items() if x != ''}
    return copy

def __convert_dates(dict_in: dict) -> dict:
    copy: dict = {x: y for (x, y) in dict_in.items()}
    myformat: str = "MMM D, YYYY @ H:mm A"
    arrow_datetime: arrow.Arrow = arrow.get(copy["date"], myformat, tzinfo=SYSTZ)
    copy["timestamp"] = int(arrow_datetime.timestamp())
    copy.pop("date")
    return copy

if __name__ == "__main__":
    in_path: pathlib.Path = pathlib.Path(cli_args.filepath)
    out_path: pathlib.Path = pathlib.Path(cli_args.outpath)

    if not in_path.exists():
        parser.error("Invalid input filepath! Check filepath and try again.")
    
    with in_path.open("r") as F:
        lines: list[str] = F.readlines()

    dr: DictReader = DictReader(lines, delimiter="\t")
    dict_rows: list[dict] = [__clean_dict(x) for x in dr]
    dict_rows = [__convert_dates(x) for x in dict_rows]

    if cli_args.console_only is True:
        for row in dict_rows:
            print(row)
    else:
        with out_path.open("w") as F:
            output_str: str = json.dumps(dict_rows)
            F.write(output_str)

    print("Program complete.")
