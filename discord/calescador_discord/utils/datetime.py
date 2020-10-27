import re
from datetime import datetime, date, time, timedelta

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

def parse_date(s: str) -> date:
    """Parses a weekday or a date in dd.mm.yyyy format."""

    try:
        return next_weekday(datetime.now().date(), parse_weekday(s))
    except ValueError:
        return datetime.strptime(s, '%d.%m.%Y').date()

def parse_weekday(s: str) -> int:
    """Parses a weekday in natural language."""
    if s == "":
        raise ValueError('Cannot parse empty string as weekday!')

    exact = WEEKDAYS.get(s.lower(), None)
    if exact != None:
        return exact

    # Try to find abbreviation
    for (name, i) in WEEKDAYS.items():
        if name.startswith(s.lower()):
            return i

    raise ValueError('Could not parse weekday!')

def parse_time(s: str) -> time:
    """Parses an hh:mm-formatted time."""

    return datetime.strptime(s, '%H:%M').time()

def next_weekday(date: date, weekday: int):
    """Fetches the next occurrence of the given weekday."""

    days_ahead = (weekday - date.weekday() + 7) % 7
    return date + timedelta(days=days_ahead)

def format_date(date: date) -> str:
    return date.strftime('%d.%m.%Y')

def format_time(time: time) -> str:
    return time.strftime('%H:%M')

def format_datetime(dt: datetime) -> str:
    return f'{format_date(dt.date())}, {format_time(dt.time())}'

def format_datetime_span(dt1: datetime, dt2: datetime) -> str:
    if dt1.date() == dt2.date():
        return f'{format_date(dt1.date())}, {format_time(dt1.time())} - {format_time(dt2.time())}'
    else:
        return f'{format_datetime(dt1)}\n{format_datetime(dt2)}'
