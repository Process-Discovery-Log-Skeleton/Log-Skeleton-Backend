"""Implementation of the next-one-way relationship algorithm."""

import os
from src.components.logic.relationship import Relationship
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery


class Next_One_Way (Relationship):
    """Implementation of the next-one-way relationship algorithm."""

    def __init__(self, log):
        """Store the traces."""
        super().__init__(log)

        self.mode = Relationship.Mode.EXISTS

    def activity_pair_matches(self, trace, activity1, activity2) -> bool:
        """Determine if the subtrace [a1, a2] occurs in trace."""
        return self.subtrace_count(trace, [activity1, activity2]) > 0


if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    n_t = Next_One_Way(log)

    print(n_t.apply())

    log2 = importer.import_file(path)

    skeleton = lsk_discovery.apply(
        log2, parameters={
            lsk_discovery.Variants.CLASSIC.value.
            Parameters.NOISE_THRESHOLD: 0})

    print(skeleton)
