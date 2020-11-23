"""Module for importing XES event logs in various formats."""
from pm4py.objects.log.importer.xes import importer as xes_importer
from tempfile import NamedTemporaryFile


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

    def import_file(self, path: str):
        """Import XES event logs from a given file."""
        log = xes_importer.apply(path)

        return log

    def import_str(self, event_log: str):
        """Import XES event logs from a given string."""
        file = self.__save_to_temp_file(event_log)

        return self.import_file(file.name)

    def import_http_query(self, request):
        """Import XES event logs from a given HTTP request."""
        data = request.data

        return self.import_str(data)
