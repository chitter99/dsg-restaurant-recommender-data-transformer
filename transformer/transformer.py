
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

class IndexedMetric:
    def __init__(self, values=[]) -> None:
        self.values = values

    def index(self, value: str) -> int:
        try:
            return self.values.index(value.lower())
        except ValueError:
            self.values.append(value.lower())
            return len(self.values) - 1

class StringTransformer:
    def __init__(self, value: str):
        self._value = value

    def ret(self) -> str:
        return str(self._value)

    def strip(self):
        self._value = self._value.strip()
        return self

    def default(self, default):
        if not self._value:
            self._value = default
        return self

    def replace(self, test, new):
        if self._value is test:
            self._value = new
        return self

    def apply(self, func):
        self._value = func(self._value)
        return self

def vas(value):
    return StringTransformer(value).strip()

def val(value):
    return StringTransformer(value)
