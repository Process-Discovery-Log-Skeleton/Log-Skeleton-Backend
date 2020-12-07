"""Event log cache.

This module can be used to cache event-logs.
The module automatically deletes cache items that don't get
accessed for more than 10 minutes.
"""

import os
import uuid
from datetime import datetime
import appdirs
import time
import _thread

# App name for caching files
__APP_NAME__ = 'Log-Skeleton-Backend'

# 1 hour = 3600 sec
__HOUR__ = 3600

# Hash store for the event-log-files.
event_store = {}

# Store a timestmp when a file gets deleted
delete_timestamps = {}

# Caching dir on the respective os
cache_dir = appdirs.user_cache_dir(__APP_NAME__)

# Make sure the cache dir exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


def __store_delete_time(id):
    """Store the id for deletion."""
    now = datetime.now()

    timestamp = datetime.timestamp(now)

    # Keep the file for one hour
    delete_timestamps[id] = timestamp + __HOUR__


def remove_overdue_event_log_entries():
    """Remove all event log that are overdue."""
    now = datetime.now()

    timestamp = datetime.timestamp(now)

    for id in delete_timestamps:
        # Check if the entry is overdue
        if delete_timestamps[id] <= timestamp:
            remove_event_log(id)


def __save_to_file(self, content: str, id: str):
    """Save a given string to a temporary file."""
    # Create a temporary file that won't get deleted
    path = os.path.join(cache_dir, id)

    with open(path, 'w+') as f:
        f.write(content)

    return path


def remove_event_log(id):
    """Remove the file for the given id."""
    os.remove(os.path.join(cache_dir, id))

    event_store[id] = None

    delete_timestamps[id] = None


def put_event_log(file) -> str:
    """Cache the event log."""
    id = uuid.uuid4().hex

    file.save(os.path.join(cache_dir, id + '.xes'))

    event_store[id] = id + '.xes'

    print('Storing file at: ' + id + '.xes')

    __store_delete_time(id)

    return id


def pull_event_log(id):
    """Pull the event-log path from the storage."""
    # Reschedule the deletion time of the event-log
    __store_delete_time(id)

    return os.path.join(cache_dir, event_store[id])


def event_log_garbage_collector():
    """Run the event-log garbage collection."""
    while True:
        remove_overdue_event_log_entries()
        print('garbage')
        time.sleep(60)


def start_event_store():
    """Start a new thread that keeps the event-log storage clean."""
    try:
        _thread.start_new_thread(event_log_garbage_collector, ())
    except:  # noqa: E722
        print("Error: unable to start thread")
