"""Test cases for the entire Log-Skeleton."""

from src.components.logic.log_skeleton import Log_Skeleton
from src.components.util.xes_importer import XES_Importer
from tests.paper_example_model import Paper_Example_Model
import os


def compare_models(model) -> bool:
    """Compare the given model to the transcripted."""
    paper_model = Paper_Example_Model.paper_example_model()

    relationships = [
        # Dictionary contains string representation
        'always_before',
        'always_after',
        'equivalence',
        'never_together',
        # 'next_both_ways',
        # 'next_one_way',
    ]

    for key in relationships:
        rel1 = model[key]
        rel2 = paper_model[key]

        rel1.sort()
        rel2.sort()

        if len(rel1) != len(rel2):
            return False

        for item1, item2 in zip(rel1, rel2):
            print(str(item1) + "  " + str(item2))
            if item1[0] != item2[0] or item1[1] != item2[1]:
                return False

    return True


def model(extended_trace):
    """Generate the LS-model."""
    importer = XES_Importer()

    path = os.path.join(
        os.path.dirname(__file__), '../res/logs/paper-example.xes')

    log, activites = \
        importer.import_file(path, [], [], extended_trace=extended_trace)

    lsk_algo = Log_Skeleton(log, activites, 0.0, extended_trace)

    return lsk_algo.apply()


def test_log_skeleton_extended():
    """Check the correctness of the algorithm."""
    log_model = model(True)

    assert compare_models(log_model)
