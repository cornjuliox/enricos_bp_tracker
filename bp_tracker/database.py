# from tinydb import TinyDB
# from .models import Event

# class BpDataProvider():
#     def __init__(self):
#         self.db = TinyDB("database.json")
#         self.events = self.db.table("events")

#     def provide(self) -> list[Event]:
#         """
#         .provide() needs to provide a ready-to-use, sorted list of Events. Latest events first.
#         """
#         raw_data: list[dict] = self.db.all()
#         data: list[dict] = sorted(raw_data, key=lambda x: x["datetime"])
#         return data 

#     def insert(self, event: Event) -> int:
#         assert isinstance(event, Event)
#         event_dict: dict = event.dict()
#         doc_id: int = self.db.insert(event_dict)
#         return doc_id
