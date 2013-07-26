import json
import dateutil.parser
import datetime
import datehelp


class State(object):
    '''Represents the current position in the image making process.'''

    def __init__(self, start_date=None, week=0):
        '''start_date: a datetime object. the origin relative to it will
            automatically be found.'''

        origin = datehelp.find_origin(start_date)
        self.start_date = origin  # date everything else will be based on
        self.last_week = week  # the oldest week/column that has no commits

    def save_to_disk(self, path="/tmp/rectangled.save"):
        state = {"start": self.start_date.isoformat(),
                 "last_week": self.last_week}

        with open(path, "w") as save_file:
            json.dump(sate, save_file)

    @classmethod
    def load_from_disk(path="/tmp/rectangled.save"):
        new_state = State()
        with open(path, "r") as save_file:
            state = json.load(save_file)
            start_date = dateutil.parser.parse(datestate["start"])
            last_week = state["last_week"]

            new_state.start_date = start_date
            new_state.last_week = last_week

        return new_state
