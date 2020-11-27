"""Class that combines all relationships and generates a log skeleton model."""

import os
from src.components.logic.relationship import Relationship
from src.components.util.xes_importer import XES_Importer
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery


class Counter(Relationship):
    """Wrapper class to calculate the equivalence relationship."""

    def __init__(self, log):
        """Init traces and convert the traces to the extended trace."""
        super().__init__(log)

    def apply(self):
        counter = {}
        for act in self.activities:
            freq = []
            for trace in self.log:
                freq.append(len(self.project_trace(trace, [act])))
            counter[act] = {'sum': sum(freq), 'min': min(freq),
                            'max': max(freq)}
        return counter


if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    skeleton = lsk_discovery.apply(
        log, parameters={
            lsk_discovery.Variants.CLASSIC.value.
            Parameters.NOISE_THRESHOLD: 0})
    print(skeleton)
    counter = Counter(log)
    print(counter.apply())
