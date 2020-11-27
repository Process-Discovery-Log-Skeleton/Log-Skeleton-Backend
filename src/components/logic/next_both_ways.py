"""Implementation of the next-one-way relationship algorithm."""

import os
from src.components.logic.next_one_way import Next_One_Way
from src.components.util.xes_importer import XES_Importer


class Next_Both_Ways (Next_One_Way):
    """Implementation of the next-both-ways relationship algorithm."""

    def apply(self):
        """Filter of the next_one_way result."""
        next_one = super().apply()
        next_both = list()

        for tup in next_one:
            for test in next_one:
                if test == (tup[1], tup[0]):
                    next_both.append(tup)

        return next_both


if __name__ == "__main__":
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../../../res/logs/running-example.xes')

    log = importer.import_file(path)

    n_o_w = Next_One_Way(log)
    print(n_o_w.apply())

    log2 = importer.import_file(path)

    n_b_w = Next_Both_Ways(log2)
    print(n_b_w.apply())
