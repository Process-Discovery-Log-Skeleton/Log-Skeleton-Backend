"""Module for importing XES event logs in various formats."""
from pm4py.objects.log.importer.xes import importer as xes_importer
from tempfile import NamedTemporaryFile
import uuid

# XES-concept extension. General identifier field of an event.
__CONCEPT_NAME__ = 'concept:name'

TRACE_START = {__CONCEPT_NAME__: uuid.uuid4().hex}
TRACE_END = {__CONCEPT_NAME__: uuid.uuid4().hex}

class XES_Importer:
    """Importer class for importing XES event logs.

    The supported types are files, strings and HTTP requests.
    """

    def __save_to_temp_file(self, content: str):
        """Save a given string to a temporary file."""
        # Create a temporary file that won't get deleted
        file = NamedTemporaryFile(delete=False)

        with open(file.name, 'w') as f:
            f.write(content)

        return file

    def import_file(self, path: str, extended_trace=True):
        """Import XES event logs from a given file."""
        log = xes_importer.apply(path)

        if extended_trace:
            for i in range(len(log)):
                log[i] = self.extended_trace(log[i])

        return log

    def import_str(self, event_log: str, extended_trace=True):
        """Import XES event logs from a given string."""
        file = self.__save_to_temp_file(event_log)

        return self.import_file(file.name)

    def import_http_query(self, request, extended_trace=True):
        """Import XES event logs from a given HTTP request."""
        data = request.data

        return self.import_str(data)

    # Trace extension
    def extract_activities(self):
        """Extract the activity set from the log."""
        activities = set()

        for trace in self.log:
            for activity in trace:
                activities.add(self.activity_concept_name(activity))

        return activities

    def extended_trace(self, trace):
        """Convert a trace to the extended trace."""
        return [TRACE_START] + trace._list + [TRACE_END]

    def activity_concept_name(self, activity) -> str:
        """Extract the concept:name of an activity."""
        return activity[__CONCEPT_NAME__]