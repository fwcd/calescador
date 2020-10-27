import re
from datetime import datetime

WEEKDAYS = {
    # English
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
    # German
    'montag': 0,
    'dienstag': 1,
    'mittwoch': 2,
    'donnerstag': 3,
    'freitag': 4,
    'samstag': 5,
    'sonntag': 6
}

def parse_date(s):
    """Parses a weekday or a date in dd.mm.yyyy format."""

    try:
        return parse_weekday(s) or datetime.strptime(s, '%d.%m.%Y').date()
    except ValueError:
        return None

def parse_weekday(s):
    """Parses a weekday in natural language."""

    exact = WEEKDAYS.get(s, None)
    if exact:
        return exact

    # Try to find abbreviation
    for weekday in WEEKDAYS:
        if weekday.startswith(s):
            return weekday

    return None

def parse_time(s):
    """Parses an hh:mm-formatted time."""

    return datetime.strptime(s, '%H:%M').time()

def next_weekday(date, weekday):
    """Fetches the next occurrence of the given weekday."""

    days_ahead = (weekday - date.weekday() + 7) % 7
    return date + datetime.timedelta(days=days_ahead)

def format_date(date):
    return date.strftime('%d.%m.%Y')

def format_time(time):
    return time.strftime('%H:%M')

def format_datetime(dt):
    return f'{format_date(dt.date())} {format_time(dt.time())}'

def format_datetime_span(dt1, dt2):
    if dt1.date() == dt2.date():
        return f'{format_date(dt1.date())} {format_time(dt1.time())} - {format_time(dt2.time())}'
    else:
        return f'{format_datetime(dt1)} - {format_datetime(dt2)}'
