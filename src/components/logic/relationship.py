# XES-concept extension. General identifier field of an event.
__CONCEPT_NAME__ = 'concept:name'

from src.components.util.xes_importer import XES_Importer

class Relationship:

    def __init__(self, traces):
        self.traces = traces


    # Activity related functions
    def activity_concept_name(self, activity):
        """
        Extract the concept:name of an activity
        """
        return activity[__CONCEPT_NAME__]

    # Trace related functions

    def project_trace(self, trace, elements):
        """
        Project the trace to a given set of activities.
        """
        activity_names = elements.map(lambda ac: self.activity_concept_name(ac))

        return trace.filter(lambda ac: activity_names.contains(self.activity_concept_name(ac)))

    def first(self, trace):
        """
        Return the first activity.
        """
        return trace[0]

    def last(self, trace):
        """
        Return the last activity.
        """
        return trace[-1]

    def count(self, trace):
        """
        Return the number of activity in that one trace.
        """
        return len(trace)

    def apply(self):
        """
        Implements one relationship algorithm.
        """
        result = []

        for trace in self.traces:
            res = self.apply_to_trace(trace)

            result.append(res)

        return res

    def apply_to_trace(self, trace):
        """
        Apply a certain algorithm to a spectific trace.
        """
        raise NotImplementedError


if __name__ == "__main__":
    
    importer = XES_Importer()

    log = importer.import_file('../../../res/logs/running-example.xes')

    print(log[0])
    print('Activity')
    print(log[0][0])