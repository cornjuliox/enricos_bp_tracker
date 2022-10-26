import json

# things this little module needs to handle gracefully:
# load from a file
# update the list of entries IN-MEMORY while the program is running
# write back to a file

# things I haven't quite decided on yet:
# how do I get the various pieces of the program to communicate with one another?
# pubsub seems like the most obvious choice but maybe there's something even
# simpler out there

class DataHandler():
    def __init__(self, *args, **kwargs):
        # DataHandler needs to provide ready-to-use, i.e sorted data
        # to components within the program. this will be the source of truth
        # for every component that uses the BP data.

        # DataHandler needs to be provided with cleaned data, ready to store
        # it shouldn't handle any of the cleaning i.e transforming the datetime
        # to a unix timestamp etc. The data passed in should be ready for storage
        # via a json.dumps() and then F.write()
        self._data: list[dict] = []
        pass

    def _startup(self):
        # load the file
        pass

    def _shutdown(self):
        # register with atexit so that this gets called when the program exits
        pass
    pass
