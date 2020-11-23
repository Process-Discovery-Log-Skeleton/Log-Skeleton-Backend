from pm4py.objects.log.importer.xes import importer as xes_importer
from tempfile import NamedTemporaryFile
from flask import request

class XES_Importer:


    def __save_to_temp_file(self, content: str):

        # Create a temporary file that won't get deleted
        file = NamedTemporaryFile(delete=False)
        
        with open(file.name, 'w') as f:
            f.write(content)

        return file


    def import_file(self, path: str):
        log = xes_importer.apply(path)

        return log


    def import_str(self, event_log: str):

        file = self.__save_to_temp_file(event_log)

        return self.import_file(file.name)


    def import_http_query(self, request):
        data = request.data

        return self.import_str(data)
