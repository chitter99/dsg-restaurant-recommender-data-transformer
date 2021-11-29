
import csv


# Transforms csv files to a customizable format
class Transformer:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def _perload_transformer(self):
        pass

    def _transform(self, row) -> dict:
        pass

    def _fieldnames(self) -> list:
        pass

    def transform(self):
        transformed_data = []
        self._perload_transformer()
        with open(self.input) as file:
            reader = csv.DictReader(file, delimiter=',', quotechar='"')
            for row in reader:
                transformed_data.append(self._transform(row))
        with open(self.output) as file:
            writer = csv.DictWriter(file, fieldnames=self._fieldnames())
            writer.writeheader()
            for row in transformed_data:
                writer.writerow(row)

# Adds id layer to transformer
class IdTransformer(Transformer):
    def _perload_transformer(self):
        self.ids = dict()
        self._id_counter = 0
        super()._perload_transformer()

    def _id(self, old_id) -> int:
        self._id_counter += 1
        self.ids[old_id] = self._id_counter
        return self._id_counter
