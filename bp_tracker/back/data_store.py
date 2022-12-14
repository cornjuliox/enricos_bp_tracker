import pathlib
import json
import logging

from typing import Any

from bp_tracker.front.utils import clamp

logger: logging.Logger = logging.getLogger(__name__)

class FlatFileWriter():
    def __init__(self, path: pathlib.Path):
        self._path: pathlib.Path = path
        self._backup: pathlib.Path = self._path.parent / (self._path.name + ".bak")

    def retrieve(self) -> list[dict[Any, Any]]:
        with self._path.open("r") as F:
            try:
                bpdata: list[dict[Any, Any]] = json.loads(F.read())
            except json.decoder.JSONDecodeError:
                bpdata = []
        
        return bpdata

    def commit(self, data: str):
        with self._path.open("w") as F:
            F.write(data)

class BPDataStore():
    def __init__(self, path: pathlib.Path):
        # self._writer = FlatFileWriter(path)
        # NOTE: maybe a separate FileHandler class for this? 
        self.path: pathlib.Path = path
        self.ffw: FlatFileWriter = FlatFileWriter(self.path)
        self._bpdata: list[dict[Any, Any]] = self.ffw.retrieve()
        logger.debug(f"self._bpdata empty? {len(self._bpdata)}")

    def _commit(self):
        logger.info("Committing new records to file.")
        prepped_data: str = json.dumps(self._bpdata)
        self.ffw.commit(prepped_data)
    
    def latest(self, limit: int = 10, ascending: bool = False) -> list[dict]:
        limit = clamp(1, limit, len(self._bpdata))
        logger.info("Retrieving latest records.")
        logger.debug(f"limit set to: {limit}")

        if ascending:
            logger.info("Returning records in ascending order, by datetime.")
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])
        else:
            logger.info("Returning records in descending order, by datetime.")
            prepped = sorted(self._bpdata, key=lambda x: x["timestamp"])[::-1]

        return prepped[:limit]

    def all(self):
        logger.info("Returning ALL records. Good luck reading all that.")
        return self._bpdata

    def date_range(self, start: int, end: int) -> list[dict]:
        logger.info("Returning records for a specific date range.")
        logger.debug(f"start time: {start}")
        logger.debug(f"end time: {end}")
        prepped: list[dict] = [x for x in self._bpdata if x["timestamp"] >= start and x["timestamp"] <= end]
        prepped = sorted(prepped, key=lambda x: x["timestamp"])[::-1]
        return prepped

    def add(self, sys: int, dia: int, pulse: int, notes: int, timestamp: int):
        logger.info("Adding a new entry")
        data: dict = {
            "sys": sys,
            "dia": dia,
            "pulse": pulse,
            "notes": notes,
            "timestamp": timestamp
        }
        logger.debug(f"raw_data: {data}")

        self._bpdata.append(data)
        self._commit()

    # NOTE: There should never be a need to 'edit' an entry, I hope.
    def remove(self, timestamp: int):
        logger.info("Removing an entry based on timestamp.")
        logger.debug(f"timestamp: {timestamp}")
        new_list: list[dict] = [x for x in self._bpdata if x.get("timestamp") != timestamp]
        self._bpdata = new_list
        self._commit()
