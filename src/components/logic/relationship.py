"""Base class for the log-skeleton relationship implementations."""

from enum import Enum
import os
import itertools
from src.components.util.xes_importer import *

# XES-concept extension. General identifier field of an event.
__CONCEPT_NAME__ = 'concept:name'

class Relationship:
    """Base class for the log-skeleton relationship implementations.

    This class can be inhertited to implement the relationship algorithms.
    It provides different kinds of helper functions to make the
    implementation of the relationship algorithm as easy as possible.
    """

    class Mode (Enum):
        """Operation mode of the apply method.

        FORALL: In a FORALL relationship the condition
        has to be true for all traces.

        EXISTS: In a EXISTS relationship the condition
        has to be true for at least one trace.
        """

        FORALL = 0
        EXISTS = 1

    def __init__(self, log, all_activities = None, noise_threshold=0.0,
            mode=Mode.FORALL, include_extenstions=False):
        """Initalizes and sets up the relationship.

        Parameters:
            log : Log of traces
            all_activities : Collection of all occuring activities
            mode (Relationship.Mode, optional): 
            Mode in which the relationship operates. Defaults to Mode.FORALL.
            include_extenstions (bool, optional): 
            Determines whether the trace extensions 
            will be included in the final set. Defaults to False.
        """

        if isinstance(log, tuple):
            self.log = log[0]
            self.activities = log[1]
        else:
            self.log = log
            self.activities = all_activities

            if all_activities is None:
                raise TypeError('all_activs should not be None!')

        self.noise_threshold = noise_threshold
        self.include_extenstions = include_extenstions

        self.mode = mode

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

    def subtrace_count(self, trace, subtrace):
        """Count the number of occurences of subtrace in trace."""
        if len(subtrace) == 0:
            return 0

        count = 0

        tr = list(map(lambda ac: self.activity_concept_name(ac), trace))

        for index in range(len(tr) - len(subtrace) + 1):
            slice = tr[index:index + len(subtrace)]

            if subtrace == slice:
                count += 1

        return count

    def first(self, trace):
        """Return the first activity."""
        return trace[0]

    def last(self, trace):
        """Return the last activity."""
        return trace[-1]

    def count(self, trace):
        """Return the number of activity in that one trace."""
        return len(trace)

    def create_relation_superset(self):
        """Create the crossproduct of the actvities."""
        # trace = [a, b, c]
        # trace x trace = [(a, a), (a, b), ..., (c, a), (c, b), (c, c)]
        return itertools.product(self.activities, self.activities)

    def apply(self):
        """Implement a relationship algorithm."""
        results = set()

        source = self.create_relation_superset()

        total_traces = len(self.log)

        if self.mode == Relationship.Mode.FORALL:  # For all condition
            for a1, a2 in source:
                res = 0
                for trace in self.log:
                    apply = self.apply_to_trace(trace, a1, a2)
                    res += 1 if apply else 0

                if res / total_traces >= (1 - self.noise_threshold):
                    results.add((a1, a2))

        elif self.mode == Relationship.Mode.EXISTS:  # Exists condition
            for a1, a2 in source:
                res = False
                for trace in self.log:
                    res = res or self.apply_to_trace(trace, a1, a2)

                    if res:
                        break

                if res:
                    results.add((a1, a2))

        return results

    def apply_to_trace(self, trace, a1, a2) -> bool:
        """Apply the matching algorithm to each pair of activities."""
        if self.activity_pair_matches(trace, a1, a2):

            if not self.include_extenstions and \
                    (self.is_extension_activity(a1)
                        or self.is_extension_activity(a2)):
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
