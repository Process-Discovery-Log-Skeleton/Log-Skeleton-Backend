""" Algorithm to detect the always after relationships in a given log """
import os
from src.components.logic.relationship import Relationship
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery


class AlwaysAfter(Relationship):
    """ Implementation of the always after relationship"""

    def __init__(self, traces):
        super().__init__(traces)

    def activity_pair_matches(self, trace, activity1, activity2) -> bool:
        """Determine if the given pair of activities in the always after condition."""

        # Non-reflexive
        if activity1 == activity2:
            return False

        activity_projection = self.project_trace(trace, [activity1, activity2])

        return activity1 not in activity_projection or activity_projection[-1] == activity2


if __name__ == '__main__':
    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/paper-example.xes')
    log = XES_Importer().import_file(path)

    always_after = AlwaysAfter(log)
    ls = lsk_discovery.apply(log, parameters={
        lsk_discovery.Variants.CLASSIC.value.Parameters.NOISE_THRESHOLD: 0.0})
    print(ls['always_after'])
    print(always_after.apply())
