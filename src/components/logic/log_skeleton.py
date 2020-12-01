"""Generates a log skeleton model based on the underlying relationships."""

import os
from src.components.logic import relationships as rel
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery


class Log_Skeleton:
    """Class that combines all relationships and generates a log skeleton."""

    def __init__(self, log, all_activities, noise_threshhold):
        """Init an instance that will generate a log skeleton model.

        Parameters:
            log : Log of traces
            all_activities : Collection of all occuring activities
            noise_threshhold : Set sentivity level for the algorithms
        """
        self.log = log
        self.relationships = {
            # Dictionary contains string representation of all classes
            rel.Always_Before: 'always_before',
            rel.AlwaysAfter: 'always_after',
            rel.Equivalence: 'equivalence',
            rel.Never_Together: 'never_together',
            rel.Next_Both_Ways: 'next_both_ways',
            rel.Next_One_Way: 'next_one_way',
            rel.Counter: 'counter',
        }
        self.all_activities = all_activities
        self.noise_threshhold = noise_threshhold

    def apply(self):
        """Return the log skeleton model as a dictionary.

        Each key contains name of the relationship.
        The corresponding value is the set with all
        activitiy pairs of that relationship.
        """
        res = {}
        for r in self.relationships:
            r_instance = r(self.log, self.all_activities,
                           self.noise_threshhold,
                           rel.Relationship.Mode.FORALL, False)
            if (r == rel.Next_One_Way):
                r_instance.mode = rel.Relationship.Mode.EXISTS
            res[self.relationships[r]] = r_instance.apply()
        return res


if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log_and_activset = importer.import_file(path)
    log = log_and_activset[0]
    activset = log_and_activset[1]

    skeleton = lsk_discovery.apply(
        log, parameters={
            lsk_discovery.Variants.CLASSIC.value.
            Parameters.NOISE_THRESHOLD: 0})
    print(skeleton)
    model = Log_Skeleton(log, activset, 0.1)
    print(model.apply())
