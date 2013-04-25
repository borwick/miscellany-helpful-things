from pytz import utc
from datetime import datetime, timedelta


def utc_dt(time_string, time_format='%Y-%m-%d %H:%M:%S'):
    """
    Default time_format likes YYYY-MM-DD HH:MM:SS:
        2012-01-01 12:00:00

    Returns an 'aware' datetime object.
    """
    naive_datetime = datetime.strptime(time_string, time_format)
    return utc.localize(naive_datetime)


def utc_now():
    """
    How soon is now?
    """
    cur_datetime = datetime.utcnow()
    return utc.localize(cur_datetime)


def xtimerange(start, end, step):
    while start <= end:
        yield start
        start += timedelta(minutes=step)


def minute_diff(start, end):
    delta_diff = end - start
    return ( delta_diff.days * 24 * 60 ) + delta_diff.seconds // 60
