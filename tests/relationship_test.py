"""Test cases for the base relationship class."""
from src.components.logic.relationship import Relationship

traces = [
    [
        {
            'concept:name': 'Test1.1'
        },
        {
            'concept:name': 'Test1.2'
        },
        {
            'concept:name': 'Test1.3'
        }
    ],
    [
        {
            'concept:name': 'Test2.1'
        },
        {
            'concept:name': 'Test2.2'
        }
    ]
]


rel = Relationship(traces=traces)


def test_activity_concept_name():
    """Test the activity concept name extractor."""
    assert rel.activity_concept_name(traces[0][0])


def test_project_trace():
    """Test the trace projection function."""
    projection = rel.project_trace(traces[0], [traces[0][0]])

    # Test the first item
    assert rel.activity_concept_name(projection[0]) == 'Test1.1'

    projection = rel.project_trace(traces[0], [])

    # Test the empty projection
    assert len(projection) == 0

    projection = rel.project_trace(traces[0], traces[0])

    assert projection == traces[0]


def test_first():
    """Test the first function of the relationship base class."""
    assert rel.first(traces[0]) == {'concept:name': 'Test1.1'}


def test_last():
    """Test the last function of the relationship base class."""
    assert rel.last(traces[0]) == {'concept:name': 'Test1.3'}


def test_count():
    """Test the count function of the relationship base class."""
    assert rel.count(traces[0]) == 3
