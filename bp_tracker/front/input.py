import argparse
import arrow

from bp_tracker.back.data_store import BPDataStore

def add(cli_args: argparse.Namespace, store: BPDataStore):
    store.add(
        sys=cli_args.sys,
        dia=cli_args.dia,
        pulse=cli_args.pulse,
        notes=cli_args.notes,
        timestamp=arrow.now().int_timestamp
    )

def remove(cli_args: argparse.Namespace, store: BPDataStore):
    timestamp: int = int(cli_args.timestamp)
    store.remove(timestamp)

