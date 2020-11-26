"""Implementation of the equivalence relationship algorithm."""

import os
from src.components.logic.relationship import Relationship
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery

class Equivalence (Relationship):
    """Wrapper class to calculate the equivalence relationship."""

    def __init__(self, log):
        """Init traces and convert the traces to the extended trace."""
        super().__init__(log)

    def activity_pair_matches(self, trace, activity1, activity2):
        """Determine if the activtiy pair has the same frequencies in the trace.""" 
        projection1 = self.project_trace(trace, [activity1])
        projection2 = self.project_trace(trace, [activity2])
        
        return (len(projection1) == len(projection2))

if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    skeleton = lsk_discovery.apply(
        log, parameters={
            lsk_discovery.Variants.CLASSIC.value.
            Parameters.NOISE_THRESHOLD: 1})
    print(skeleton)
    eq = Equivalence(log)
    print(eq.apply())
	