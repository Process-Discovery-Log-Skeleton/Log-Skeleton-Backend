from pm4py.objects.log.importer.xes import importer as xes_importer
from tempfile import NamedTemporaryFile

class XES_Importer:

    def __save_to_temp_file(self, content: str):

        # Create a temporary file that won't get deleted
        file = NamedTemporaryFile(delete=False)
        
        with open(file.name, 'w') as f:
            f.write(content)

        return file

    def import_file(self, path: str):
        log = xes_importer.apply(path)

        print(log[0])

        print(log[0][0])

    def import_str(self, event_log: str):

        file = self.__save_to_temp_file(event_log)

        self.import_file(file.name)
        


if __name__ == "__main__":
    importer = XES_Importer()

    with open('./res/logs/running-example.xes') as f:
        content = f.read()
        
        importer.import_str(content)

        






