"""Base class for the log-skeleton relationship implementations."""

import os
import uuid
import itertools
from src.components.util.xes_importer import XES_Importer

# XES-concept extension. General identifier field of an event.
__CONCEPT_NAME__ = 'concept:name'

TRACE_START = {__CONCEPT_NAME__: uuid.uuid4().hex}
TRACE_END = {__CONCEPT_NAME__: uuid.uuid4().hex}

class Relationship:
    """Base class for the log-skeleton relationship implementations.

    This class can be inhertited to implement the relationship algorithms.
    It provides different kinds of helper functions to make the
    implementation of the relationship algorithm as easy as possible.
    """

    def __init__(self, log, extended=False):
        """Store the traces."""
        self.log = log

        if extended:
            self.log = map(lambda trace: self.extended_trace(trace), log)

    def extended_trace(self, trace):
        """Convert a trace to the extended trace"""
        return [TRACE_START] + trace + [TRACE_END]

    # Activity related functions
    def activity_concept_name(self, activity):
        """Extract the concept:name of an activity."""
        return activity[__CONCEPT_NAME__]

    # Trace related functions
    def is_empty(self, trace):
        """Return whether the trace is empty."""
        return len(trace) == 0

    def project_trace(self, trace, elements):
        """Project the trace to a given set of activities."""
        activity_names = list(
            map(lambda ac: self.activity_concept_name(ac), elements))

        res = filter(
            lambda ac: self.activity_concept_name(ac) in activity_names, trace)

        return list(res)

    def first(self, trace):
        """Return the first activity."""
        return trace[0]

    def last(self, trace):
        """Return the last activity."""
        return trace[-1]

    def count(self, trace):
        """Return the number of activity in that one trace."""
        return len(trace)

    def apply(self):
        """Implement a relationship algorithm."""
        results = []

        for trace in self.log:
            res = self.apply_to_trace(trace)

            results.append(res)

        # Flatten out the list
        # Each apply_to_trace returns a list of results.
        #   results might look like -> [[(a, b), (b, c)], [(b, d)], [(c, a)]]
        # Flattening this example leads to: [(a, b), (b, c), (b, d), (c, a)]
        flattenedResult = [val for traceRes in results for val in traceRes]

        return flattenedResult

    def apply_to_trace(self, trace):
        """Apply the matching algorithm to each pair of activities."""

        # trace = [a, b, c]
        # trace x trace = [(a, a), (a, b), ..., (c, a), (c, b), (c, c)]
        source = list(itertools.product(trace, trace))

        result = []

        for a1, a2 in source:
            if self.activity_pair_matches(a1, a2):
                result.append((a1, a2))
        
        return result

    def activity_pair_matches(self, activity1, activity2):
        """Determine if the given pair of activities is in the result."""
        raise NotImplementedError

if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    print(log[0])
    print('Activity')
    print(log[0][0])
