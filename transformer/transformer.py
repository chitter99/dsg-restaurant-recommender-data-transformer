
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

    # helper functions
    def _rename(self, row, transforms=dict()):
        trow = dict()
        for old_col in transforms.keys():
            trow[transforms[old_col]] = row[old_col]
        return trow

    def transform(self):
        transformed_data = []
        self._perload_transformer()
        with open(self.input, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file, delimiter=',', quotechar='"')
            for row in reader:
                transformed_data.append(self._transform(row))
        with open(self.output, 'w+', newline='', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, delimiter=',', 
                quotechar='"', fieldnames=self._fieldnames())
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
