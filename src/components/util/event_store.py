"""Event log cache.

This module can be used to cache event-logs.
The module automatically deletes cache items that don't get
accessed for more than 10 minutes.
"""

from os import times, path
from tempfile import NamedTemporaryFile
import uuid
from datetime import date, datetime
from appdirs import *
import sched, time
import flask

# App name for caching files
__APP_NAME__ = 'Log-Skeleton-Backend'

# 10 minutes = 600 sec
__10_MINUTES__ = 600

# Hash store for the event-log-files.
event_store = {}

# Store a timestmp when a file gets deleted
delete_timestamps = {}

# Caching dir on the respective os
cache_dir = user_cache_dir(__APP_NAME__)

s = sched.scheduler(time.time, time.sleep)

# Make sure the cache dir exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

def __store_delete_time(id):
    """Store the id for deletion."""
    now = datetime.now()
    
    timestamp = datetime.timestamp(now)

    # Keep the file for one hour
    delete_timestamps[id] = timestamp + __10_MINUTES__


def remove_overdue_event_log_entries(sc):
    """Remove all event log that are overdue."""
    now = datetime.now()

    timestamp = datetime.timestamp(now)

    for id in delete_timestamps:
        # Check if the entry is overdue
        if delete_timestamps[id] <= timestamp:
            remove_event_log(id)
    
    # Reschedule the task
    s.enter(60, 1, remove_overdue_event_log_entries, (s,))


def __save_to_file(self, content: str, id: str):
    """Save a given string to a temporary file."""
    # Create a temporary file that won't get deleted
    path = os.path.join(cache_dir, id)

    with open(path, 'w+') as f:
        f.write(content)

    return path


def remove_event_log(id):
    """Remove the file for the given id"""
    os.remove(os.path.join(cache_dir, id))

    event_store[id] = None

    delete_timestamps[id] = None


def put_event_log(file) -> str:
    
    id = uuid.uuid4().hex

    file.save(os.path.join(cache_dir, id + '.xes'))


    event_store[id] = id + '.xes'

    print('Storing file at: ' + id + '.xes')

    __store_delete_time(id)

    return id


def pull_event_log(id):

    # Reschedule the deletion time of the event-log
    __store_delete_time(id)

    return os.path.join(cache_dir, event_store[id])


def start_event_store():

    s.enter(60, 1, remove_overdue_event_log_entries, (s,))
    s.run()
