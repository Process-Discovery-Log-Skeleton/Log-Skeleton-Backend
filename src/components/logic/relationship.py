"""Base class for the log-skeleton relationship implementations."""
# XES-concept extension. General identifier field of an event.
__CONCEPT_NAME__ = 'concept:name'

from src.components.util.xes_importer import XES_Importer


class Relationship:
    """Base class for the log-skeleton relationship implementations.

    This class can be inhertited to implement the relationship algorithms.
    It provides different kinds of helper functions to make the
    implementation of the relationship algorithm as easy as possible.
    """

    def __init__(self, traces):
        """Store the traces."""
        self.traces = traces

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
        result = []

        for trace in self.traces:
            res = self.apply_to_trace(trace)

            result.append(res)

        return result

    def apply_to_trace(self, trace):
        """Apply a certain algorithm to a spectific trace."""
        raise NotImplementedError


if __name__ == "__main__":
    importer = XES_Importer()

    log = importer.import_file('../../../res/logs/running-example.xes')

    print(log[0])
    print('Activity')
    print(log[0][0])
