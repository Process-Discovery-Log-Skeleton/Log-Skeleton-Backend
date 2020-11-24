from src.components.logic.relationship import Relationship

traces = [
    {
        'events': [
            {
                'concept:name': 'Test1'
            },
            {
                'concept:name': 'Test2'
            }
        ]
    },
    {
        'events': [
            {
                'concept:name': 'Test1'
            },
            {
                'concept:name': 'Test2'
            }
        ]
    }
]

rel = Relationship(traces=traces)
