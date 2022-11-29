import argparse
import arrow
import logging

from bp_tracker.back.data_store import BPDataStore
from bp_tracker.front.utils import SYSTZ

logger = logging.getLogger(__name__)

def add(cli_args: argparse.Namespace, store: BPDataStore):
    if cli_args.datetime is not None:
        logger.debug("Using override timestamp.")
        formatstr: str = "MMM D, YYYY @ H:mm A"
        raw_datetime: arrow.Arrow = arrow.get(
            cli_args.datetime,
            formatstr,
            tzinfo=SYSTZ
        )
        timestamp: int = raw_datetime.int_timestamp
        logger.debug(f"timestamp: {timestamp}")
    else:
        logger.debug("Using current time.")
        timestamp: int = arrow.now(SYSTZ).int_timestamp
        logger.debug(f"timestamp: {timestamp}")

    store.add(
        sys=cli_args.sys,
        dia=cli_args.dia,
        pulse=cli_args.pulse,
        notes=cli_args.notes,
        timestamp=timestamp
    )

def remove(cli_args: argparse.Namespace, store: BPDataStore):
    timestamp: int = int(cli_args.timestamp)
    store.remove(timestamp)

