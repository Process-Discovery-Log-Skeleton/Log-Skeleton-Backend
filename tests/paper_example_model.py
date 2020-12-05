"""Log Skeleton Model transcribed from the Log Skeleton paper."""

from src.components.util.xes_importer \
    import TRACE_START, TRACE_END, CONCEPT_NAME


class Paper_Example_Model:
    """Log Skeleton Model transcribed from the Log Skeleton paper."""

    @staticmethod
    def paper_example_model():
        """Return the model."""
        model = {
            'equivalence': [
                (TRACE_START[CONCEPT_NAME], TRACE_START[CONCEPT_NAME]),
                (TRACE_START[CONCEPT_NAME], TRACE_END[CONCEPT_NAME]),
                (TRACE_START[CONCEPT_NAME], 'a1'),
                ('a1', 'a1'),
                ('a1', TRACE_START[CONCEPT_NAME]),
                ('a1', TRACE_END[CONCEPT_NAME]),
                ('a2', 'a2'),
                ('a3', 'a3'),
                ('a4', 'a4'),
                ('a4', 'a5'),
                ('a5', 'a5'),
                ('a5', 'a4'),
                ('a6', 'a6'),
                ('a7', 'a7'),
                ('a8', 'a8'),
                (TRACE_END[CONCEPT_NAME], TRACE_END[CONCEPT_NAME]),
                (TRACE_END[CONCEPT_NAME], TRACE_START[CONCEPT_NAME]),
                (TRACE_END[CONCEPT_NAME], 'a1')
            ],
            'always_after': [
                (TRACE_START[CONCEPT_NAME], 'a1'),
                (TRACE_START[CONCEPT_NAME], 'a4'),
                (TRACE_START[CONCEPT_NAME], 'a5'),
                (TRACE_START[CONCEPT_NAME], TRACE_END[CONCEPT_NAME]),
                ('a1', 'a4'),
                ('a1', 'a5'),
                ('a1', TRACE_END[CONCEPT_NAME]),
                ('a2', 'a5'),
                ('a2', TRACE_END[CONCEPT_NAME]),
                ('a3', 'a5'),
                ('a3', TRACE_END[CONCEPT_NAME]),
                ('a4', 'a5'),
                ('a4', TRACE_END[CONCEPT_NAME]),
                ('a5', TRACE_END[CONCEPT_NAME]),
                ('a6', 'a4'),
                ('a6', 'a5'),
                ('a6', TRACE_END[CONCEPT_NAME]),
                ('a7', TRACE_END[CONCEPT_NAME]),
                ('a8', TRACE_END[CONCEPT_NAME])
            ],
            'always_before': [
                ('a1', TRACE_START[CONCEPT_NAME]),
                ('a2', TRACE_START[CONCEPT_NAME]),
                ('a3', TRACE_START[CONCEPT_NAME]),
                ('a4', TRACE_START[CONCEPT_NAME]),
                ('a5', TRACE_START[CONCEPT_NAME]),
                ('a6', TRACE_START[CONCEPT_NAME]),
                ('a7', TRACE_START[CONCEPT_NAME]),
                ('a8', TRACE_START[CONCEPT_NAME]),
                (TRACE_END[CONCEPT_NAME], TRACE_START[CONCEPT_NAME]),
                ('a2', 'a1'),
                ('a3', 'a1'),
                ('a4', 'a1'),
                ('a5', 'a1'),
                ('a6', 'a1'),
                ('a7', 'a1'),
                ('a8', 'a1'),
                (TRACE_END[CONCEPT_NAME], 'a1'),
                ('a5', 'a4'),
                ('a6', 'a4'),
                ('a7', 'a4'),
                ('a8', 'a4'),
                (TRACE_END[CONCEPT_NAME], 'a4'),
                ('a6', 'a5'),
                ('a7', 'a5'),
                ('a8', 'a5'),
                (TRACE_END[CONCEPT_NAME], 'a5')
            ],
            'never_together': [
                ('a7', 'a8'),
                ('a8', 'a7')
            ],
            'counter': {
                TRACE_START[CONCEPT_NAME]: {'sum': 20, 'min': 1, 'max': 1},
                'a1': {'sum': 20, 'min': 1, 'max': 1},
                'a2': {'sum': 20, 'min': 0, 'max': 3},
                'a3': {'sum': 14, 'min': 0, 'max': 2},
                'a4': {'sum': 34, 'min': 1, 'max': 4},
                'a5': {'sum': 34, 'min': 1, 'max': 4},
                'a6': {'sum': 14, 'min': 0, 'max': 3},
                'a7': {'sum': 9, 'min': 0, 'max': 1},
                'a8': {'sum': 11, 'min': 0, 'max': 1},
                TRACE_END[CONCEPT_NAME]: {'sum': 14, 'min': 1, 'max': 1}
            }
        }
        return model


if __name__ == "__main__":

    model = Paper_Example_Model()
    print(model.paper_example_model())
