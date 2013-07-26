from datetime import datetime, timedelta


def find_origin(date):
    '''Find the origin sunday given a day in the current week'''

    last_sunday = (date - timedelta(days=date.weekday()) + 
                   timedelta(days=6, weeks=-1))
    origin_sunday = last_sunday + timedelta(weeks=-51)
    return origin_sunday


def find_end(date):
    '''Find the ending saturday relative to date'''

    if date is None:
       date = datetime.now()
    next_saturday = (date - timedelta(days=date.weekday()) +
                     timedelta(days=5))
    return next_saturday


def dates_for_column(week, start_date):
    '''week: a value from 0 to 51, relative to the origin date'''

    origin = find_origin(start_date)
    week_start = origin + timedelta(weeks=week)  # find the starting sunday
    
    # needs to be cleaner, oh well
    dates = []
    i = 0
    while (i < 7):
        dates.append(week_start + timedelta(days=i))
        i += 1

    return dates
