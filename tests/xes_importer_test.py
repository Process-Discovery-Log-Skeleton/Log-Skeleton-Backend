"""Tests for the xes_importer module.

The tests contain:
    - importing by string
    - importing by file
"""
from pm4py.objects.log.importer.xes import importer as xes_importer
from src.components.util.xes_importer import XES_Importer
import os


def load_example_event_log() -> str:
    """Load an example event log for testing."""
    path = os.path.join(
        os.path.dirname(__file__), '../res/logs/running-example.xes')

    with open(path, 'r') as f:
        return f.read()


def test_import_by_str():
    """Test the XES string importer."""
    importer = XES_Importer()

    log = load_example_event_log()

    # Import the event log via the importer
    event_log, ac, filt = \
        importer.import_str(log, [], [], extended_trace=False)

    path = os.path.join(
        os.path.dirname(__file__), '../res/logs/running-example.xes')

    # Import the event log via the PM4PY importer
    comparison_log = xes_importer.apply(path)

    equal = True

    # Compare the two imports
    for l1, l2 in zip(event_log, comparison_log):
        for tr1, tr2 in zip(l1, l2):
            if tr1 != tr2:
                equal = False

    assert equal


def test_import_by_file():
    """Test the XES file importer."""
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../res/logs/running-example.xes')

    # Import the event log via the importer
    event_log, activites, filt = \
        importer.import_file(path, [], [], extended_trace=False)

    # Import the event log via the PM4PY importer
    comparison_log = xes_importer.apply(path)

    equal = True

    # Compare the two imports
    for l1, l2 in zip(event_log, comparison_log):
        for tr1, tr2 in zip(l1, l2):
            if tr1 != tr2:
                equal = False

    assert equal
