import arrow
import argparse
from collections.abc import Callable

from rich.console import Console
from rich.table import Table

from bp_tracker.back.data_store import BPDataStore
from bp_tracker.front.report_generator import ReportGenerator
from bp_tracker.front.utils import (
    make_readable_timestamps,
    make_print_ready,
    create_table,
    data_prep_pipeline,
)

CONSOLE: Console = Console()

def latest(cli_args: argparse.Namespace, store: BPDataStore):
    limit: int = cli_args.limit or 10
    raw_rows: list[dict] = store.latest(limit)

    table: Table = create_table(
        title=f"Latest {len(raw_rows)} blood pressure measurements, most recent first.",
        columns=["Sys", "Dia", "Pulse", "Notes", "Timestamp"]
    )

    # NOTE: order matters!
    transformers: list[Callable] = []

    if cli_args.raw_timestamps is not True:
        transformers.append(make_readable_timestamps)

    transformers.append(make_print_ready)
    ready_rows: list[dict] = data_prep_pipeline(raw_rows, transformers)

    for x in ready_rows:
        # NOTE: maybe consider using the starred expression
        # NOTE: counter - * expression might not preserve the order of the values,
        #       which is important to the order they appear in the tables.
        table.add_row(
            x["sys"],
            x["dia"],
            x["pulse"],
            x["notes"],
            x["timestamp"]
        )

    CONSOLE.print(table)

def month(cli_args: argparse.Namespace, store: BPDataStore):
    month_int: int = cli_args.month_int
    year_int: int = cli_args.year_int

    target_arrow: arrow.Arrow = arrow.get(f"{month_int}-{year_int}", "M-YYYY")
    end_arrow: arrow.Arrow = target_arrow.shift(months=1)

    table: Table = create_table(
        title=f"Blood pressure data for the month of {target_arrow.format('MMMM YYYY')}",
        columns=["Sys", "Dia", "Pulse", "Notes", "Timestamp"]
    )

    transformers: list[Callable] = [make_readable_timestamps, make_print_ready]
    ready_rows: list[dict] = store.date_range(target_arrow.int_timestamp, end_arrow.int_timestamp)
    ready_rows = data_prep_pipeline(ready_rows, transformers)

    for x in ready_rows:
        table.add_row(x["sys"], x["dia"], x["pulse"], x["notes"], x["timestamp"])

    CONSOLE.print(table)

def date_range(cli_args: argparse.Namespace, store: BPDataStore):
    start_date: str = cli_args.start_date
    end_date: str = cli_args.end_date

    # NOTE: Small note re: the end_date here, passing in `2022-07-01 2022-10-31` as args
    #       implies to laymen that you want everything starting from July 1 to the _end of oct 31_
    #       But unless you manually shift `end_arrow` to the next day (November 1 technically)
    #       it will exclude everything from Oct 31.
    # NOTE: The reason for this is because arrow.get(end_date) will return `2022-10-31 @ 00:00:00+00:00`
    #       which basically excludes everything on the day of that date.
    # NOTE: The solution is to shift the end date by 1 day.
    start_arrow: arrow.Arrow = arrow.get(start_date)
    end_arrow: arrow.Arrow = arrow.get(end_date).shift(days=1)

    start_int: int = start_arrow.int_timestamp
    end_int: int = end_arrow.int_timestamp

    transformers: list[Callable] = [make_readable_timestamps, make_print_ready]
    ready_rows: list[dict] = store.date_range(start_int, end_int)
    ready_rows = data_prep_pipeline(ready_rows, transformers)

    table: Table = create_table(
        title=f"Blood pressure data starting from {start_arrow.format('YYYY-MM-DD')} to {end_arrow.format('YYYY-MM-DD')}",
        columns=["sys", "dia", "pulse", "notes", "timestamp"]
    )

    for x in ready_rows:
        table.add_row(x["sys"], x["dia"], x["pulse"], x["notes"], x["timestamp"])

    if cli_args.report:
        rep: ReportGenerator = ReportGenerator()
        rep.generate_report(ready_rows)
    else:
        CONSOLE.print(table)
