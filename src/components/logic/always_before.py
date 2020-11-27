"""Implementation of the never-together relationship algorithm."""

import os
from src.components.logic.relationship import Relationship
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery


class Always_Before (Relationship):
    """Implementation of the always-before relationship."""

    def __init__(self, traces):
        """Init traces and convert the traces to the extended trace."""
        super().__init__(traces)

    def activity_pair_matches(self, trace, activity1, activity2):
        """Determine if the activtiy pair matches the always_before relationship.""" 
        projection1 = self.project_trace(trace, [activity1])
        projection2 = self.project_trace(trace, [activity1, activity2])

        return (self.is_empty(projection1) or self.first(projection2) == activity2)

if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    a_b = Always_Before(log)

    print(a_b.apply())

    skeleton = lsk_discovery.apply(
        log, parameters={
            lsk_discovery.Variants.CLASSIC.value.
            Parameters.NOISE_THRESHOLD: 1.0})

    print(skeleton)
