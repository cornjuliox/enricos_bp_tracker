import pathlib
import json


class BPDataStore():
    def __init__(self, path: pathlib.Path):
        # NOTE: maybe a separate FileHandler class for this? 
        self.path = path
        if self.path.exists():
            with self.path.open("r") as F:
                self._bpdata: list[dict] = json.loads(F.read())
        else:
            self._bpdata: list[dict] = {}

    # NOTE: I'm surprised python doesn't come with a builtin that does this but hey.
    def _clamp(self, minimum, val, maximum):
        return max(minimum, min(val, maximum))

    def _commit(self):
        with self.path.open("w") as F:
            F.write(json.dumps(self._bpdata))
    
    def latest(self, limit: int = 10, ascending: bool = False) -> list[dict]:
        limit: int = self._clamp(1, limit, len(self._bpdata))

        if ascending:
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])
        else:
            prepped: list[dict] = sorted(self._bpdata, key=lambda x: x["timestamp"])[::-1]

        return prepped[:limit]

    def all(self):
        return self._bpdata

    def date_range(self, start: int, end: int) -> list[dict]:
        prepped: list[dict] = [x for x in self._bpdata if x["timestamp"] >= start and x["timestamp"] <= end]
        prepped: list[dict] = sorted(prepped, key=lambda x: x["timestamp"])[::-1]
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
