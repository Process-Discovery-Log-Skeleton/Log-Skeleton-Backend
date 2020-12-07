"""Module for importing XES event logs in various formats."""
from pm4py.objects.log.importer.xes import importer as xes_importer
from tempfile import NamedTemporaryFile
import uuid

# XES-concept extension. General identifier field of an event.
CONCEPT_NAME = 'concept:name'

TRACE_START = {CONCEPT_NAME: uuid.uuid4().hex}
TRACE_END = {CONCEPT_NAME: uuid.uuid4().hex}


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

    def import_file(self, path: str, forbidden, required, extended_trace=True):
        """Import XES event logs from a given file.

        Returns:
            A tuple containing the imported log alongside
            the set of activites.
        """
        log = xes_importer.apply(path)

        if extended_trace:
            for i in range(len(log)):
                log[i] = self.extended_trace(log[i])

        activites = self.extract_activities(log, forbidden)

        filtered_log = self.filter_log(log, forbidden, required)

        return (filtered_log, activites)

    def import_str(self, event_log: str,
                   forbidden, required, extended_trace=True):
        """Import XES event logs from a given string.

        Returns:
            A tuple containing the imported log alongside
            the set of activites.
        """
        file = self.__save_to_temp_file(event_log)

        return self.import_file(file.name,
                                forbidden,
                                required,
                                extended_trace=extended_trace)

    def import_http_query(self, request,
                          forbidden, required, extended_trace=True):
        """Import XES event logs from a given HTTP request.

        Returns:
            A tuple containing the imported log alongside
            the set of activites.
        """
        data = str(request.data, 'utf-8')

        return self.import_str(data,
                               forbidden,
                               required,
                               extended_trace=extended_trace)

    # Trace extension
    def extract_activities(self, log, forbidden):
        """Extract the activity set from the log."""
        activities = set()

        for trace in log:
            for activity in trace:
                name = self.activity_concept_name(activity)
                if name not in forbidden:
                    activities.add(name)

        return activities

    def include_trace(self, trace, forbidden, required):
        """Decide whether the trace will be included or not."""
        mapped_trace = map(lambda ac:
                           self.activity_concept_name(ac), trace)

        for ac in forbidden:
            if ac in mapped_trace:
                return False

        for ac in required:
            if not (ac in mapped_trace):
                return False

        return True

    def filter_log(self, log, forbidden, required):
        """Filter all forbidden/ required activities.

        A trace will only be included in case all the required
        activities are included and none of the forbidden is included.
        """
        filtered_log = []

        for trace in log:
            if self.include_trace(trace, forbidden, required):
                filtered_log.append(trace)

        return filtered_log

    def extended_trace(self, trace):
        """Convert a trace to the extended trace."""
        return [TRACE_START] + trace._list + [TRACE_END]

    def activity_concept_name(self, activity) -> str:
        """Extract the concept:name of an activity."""
        return activity[CONCEPT_NAME]
