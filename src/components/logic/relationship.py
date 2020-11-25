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

    def __init__(self, log):
        """Store the traces."""
        self.log = log
        self.activities = self.extract_activities()

    def extract_activities(self):
        """Extract the activity set from the log."""
        activities = set()

        for trace in self.log:
            for activity in trace:
                activities.add(self.activity_concept_name(activity))

        return activities

    def extended_trace(self, trace):
        """Convert a trace to the extended trace."""
        return [TRACE_START] + trace + [TRACE_END]

    # Activity related functions
    def activity_concept_name(self, activity) -> str:
        """Extract the concept:name of an activity."""
        return activity[__CONCEPT_NAME__]

    def is_start(self, activity) -> bool:
        """Determine whether an activity is the start activity."""
        return activity == self.activity_concept_name(TRACE_START)

    def is_end(self, activity) -> bool:
        """Determine whether an activity is the end activity."""
        return activity == self.activity_concept_name(TRACE_END)

    def is_extension_activity(self, activity) -> bool:
        """Determine whether an activity is one of the extension activities."""
        return self.is_start(activity) or self.is_end(activity)

    # Trace related functions
    def is_empty(self, trace) -> bool:
        """Return whether the trace is empty."""
        return len(trace) == 0

    def project_trace(self, trace, elements):
        """Project the trace to a given set of activities."""
        res = filter(
            lambda ac: self.activity_concept_name(ac) in elements, trace)

        return list(map(lambda ac: self.activity_concept_name(ac), res))

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

        # trace = [a, b, c]
        # trace x trace = [(a, a), (a, b), ..., (c, a), (c, b), (c, c)]
        source = itertools.product(self.activities, self.activities)

        for a1, a2 in source:
            res = True
            for trace in self.log:
                res = res and self.apply_to_trace(trace, a1, a2)

            if res:
                results.append((a1, a2))

        # Flatten out the list
        # Each apply_to_trace returns a list of results.
        #   results might look like -> [[(a, b), (b, c)], [(b, d)], [(c, a)]]
        # Flattening this example leads to: [(a, b), (b, c), (b, d), (c, a)]
        # flattenedResult = [val for traceRes in results for val in traceRes]

        return results

    def apply_to_trace(self, trace, a1, a2) -> bool:
        """Apply the matching algorithm to each pair of activities."""
        if self.activity_pair_matches(trace, a1, a2):

            if self.is_extension_activity(a1) \
                    or self.is_extension_activity(a2) or a1 == a2:
                return False

            return True

        return False

    def activity_pair_matches(self, trace, activity1, activity2) -> bool:
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
