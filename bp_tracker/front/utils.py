import arrow
import datetime
from typing import Optional
from datetime import tzinfo
from collections.abc import Callable

from rich.table import Table

# NOTE: This is needed to convert timestamps to the correct local timezone.
# NOTE: It's also really ugly looking lol
# NOTE: Now that I'm using mypy it complains about this line being Optional[tzinfo]
#       but the argument passed to arrow.to() needs to be Union[tzinfo, str]
# NOTE: This led me down a rabbit hole - apparently being able to get a local timezone is not
#       a guarantee, so all assumptions I made re: anything regarding the "time" is wrong.
# NOTE: I might need to re-tool the whole timestamp thing to account for the possibility
#       that there may not be a way to get a timezone.
SYSTZ: Optional[tzinfo] = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

def clamp(minimum, val, maximum):
    return max(minimum, min(val, maximum))

# NOTE: I might consider making a special class to encapsulate and highlight
#       the special purpose that these functions have.
#       e.g `class Transformer`, and then override `__call__()`
def make_readable_timestamps(rows: list[dict]) -> list[dict]:
    def __convert_timestamp(x: dict) -> dict:
        int_timestamp: int = x["timestamp"]
        arrow_timestamp: arrow.Arrow = arrow.get(int_timestamp)
        arrow_timestamp = arrow_timestamp.to(SYSTZ)
        x["timestamp"] = arrow_timestamp.format("MMM DD, YYYY @ HH:mm")
        return x

    rows_copy: list[dict] = [__convert_timestamp(x) for x in rows]
    return rows_copy

def make_print_ready(rows: list[dict]) -> list[dict]:
    def __stringify_everything(x: dict) -> dict:
        y: dict = {
            key: str(val)
            for (key, val) in x.items()
        }
        return y

    rows_copy: list[dict] = [__stringify_everything(x) for x in rows]
    return rows_copy

def create_table(title: str = "", columns: list[str] = None) -> Table:
    # NOTE: Future expansion of this function can include shit for
    #       styling and stuff.
    tab: Table = Table(title=title)

    for col in columns:
        tab.add_column(col)

    return tab

def data_prep_pipeline(data: list[dict], makes: list[Callable]):
    # NOTE: In case it's not obvious the point is to apply a list of functions that transform
    #       a list[dict] repeatedly.
    # NOTE: Somehow I feel like I'm overcomplicating this but hey whatever.
    while True:
        try:
            func = makes.pop(0)
        except IndexError:
            break
        
        data = func(data)
    return data
