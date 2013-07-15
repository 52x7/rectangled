from datetime import datetime, timedelta

class Datehelper(object):
    @classmethod
    def find_origin(self, date):
        '''Find the origin sunday given a day in the current week'''
        
        last_sunday = (date - timedelta(days=date.weekday()) + 
                       timedelta(days=6, weeks=-1))
        origin_sunday = last_sunday + timedelta(weeks=-51)
        return origin_sunday

    @classmethod
    def find_end(self, date):
        '''Find the ending saturday relative to date'''

        if date is None:
           date = datetime.now()
        next_saturday = (date - timedelta(days=date.weekday()) +
                         timedelta(days=5))
        return next_saturday
        
    def __init__(self):
        self.origin = Datehelper.find_origin(datetime.now())
        self.end = Datehelper.find_end(datetime.now())
