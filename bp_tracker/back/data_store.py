import pathlib
import json
import logging

from typing import Any

logger: logging.Logger = logging.getLogger(__name__)

class FlatFileWriter():
    def __init__(self, path: pathlib.Path):
        self._path: pathlib.Path = path
        self._backup: pathlib.Path = self._path.parent / (self._path.name + ".bak")

    def retrieve(self) -> list[dict]:
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
        self._writer = FlatFileWriter(path)
        # NOTE: maybe a separate FileHandler class for this? 
        self.path: pathlib.Path = path
        with self.path.open("r") as F:
            try:
                self._bpdata: list[dict[Any, Any]] = json.loads(F.read())
            except json.decoder.JSONDecodeError:
                self._bpdata = [] 

        logger.debug(f"self._bpdata empty? {len(self._bpdata)}")

    # NOTE: I'm surprised python doesn't come with a builtin that does this but hey.
    # TODO: move this out into the utils lib, I think its better there
    def _clamp(self, minimum, val, maximum):
        return max(minimum, min(val, maximum))

    def _commit(self):
        with self.path.open("w") as F:
            F.write(json.dumps(self._bpdata))
    
    def latest(self, limit: int = 10, ascending: bool = False) -> list[dict]:
        limit = self._clamp(1, limit, len(self._bpdata))

        if ascending:
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])
        else:
            prepped = sorted(self._bpdata, key=lambda x: x["timestamp"])[::-1]

        return prepped[:limit]

    def all(self):
        return self._bpdata

    def date_range(self, start: int, end: int) -> list[dict]:
        prepped: list[dict] = [x for x in self._bpdata if x["timestamp"] >= start and x["timestamp"] <= end]
        prepped = sorted(prepped, key=lambda x: x["timestamp"])[::-1]
        return prepped

    def add(self, sys: int, dia: int, pulse: int, notes: int, timestamp: int):
        data: dict = {
            "sys": sys,
            "dia": dia,
            "pulse": pulse,
            "notes": notes,
            "timestamp": timestamp
        }

        self._bpdata.append(data)
        self._commit()

    # NOTE: There should never be a need to 'edit' an entry, I hope.
    def remove(self, timestamp: int):
        new_list: list[dict] = [x for x in self._bpdata if x.get("timestamp") != timestamp]
        self._bpdata = new_list
        self._commit()
