
from os.path import join
from transformer.transformer import IdTransformer, IndexedMetric, Transformer, val, vas

class Dbo:
    def __init__(self) -> None:
        self.gender = IndexedMetric('gender', ['none', 'female', 'male', 'non-binary'])
        self.alcohol_consumption = IndexedMetric('alcohol_consumption', ['nein', 'ja'])
        self.diet = IndexedMetric('diet', ['keine' 'vegetarian', 'vegan', 'pescatarian'])
        self.beverage_preference_1 = IndexedMetric('beverage_preference_1')
        self.beverage_preference_2 = IndexedMetric('beverage_preference_2')
        self.marital_status = IndexedMetric('marital_status')
        self.children = IndexedMetric('children', ['nein', 'ja'])
        self.student = IndexedMetric('student', ['nein', 'ja'])
        self.employee = IndexedMetric('employee', ['nein', 'ja'])
        self.intolerance = IndexedMetric('intolerance')
        self.religious_preference = IndexedMetric('religious_preference')
        self.smoking_area = IndexedMetric('smoking_area', ['nein', 'ja'])
        self.takeaway = IndexedMetric('takeaway', ['nein', 'ja'])
        self.seats_inside = IndexedMetric('seats_inside', ['nein', 'ja'])
        self.seats_outside = IndexedMetric('seats_outside', ['nein', 'ja'])
        self.restaurant_type_1 = IndexedMetric('restaurant_type_1')
        self.restaurant_type_2 = IndexedMetric('restaurant_type_2')
        self.cuisine_type_1 = IndexedMetric('cuisine_type_1')
        self.cuisine_type_2 = IndexedMetric('cuisine_type_2')
        self.cuisine_region_1 = IndexedMetric('cuisine_region_1')
        self.cuisine_region_2 = IndexedMetric('cuisine_region_2')
        self.vegetarian = IndexedMetric('vegetarian', ['nein', 'ja'])
        self.vegen = IndexedMetric('vegen', ['nein', 'ja'])
        self.vegetarian = IndexedMetric('vegetarian', ['nein', 'ja'])
        self.breakfast = IndexedMetric('breakfast', ['nein', 'ja'])
        self.brunch = IndexedMetric('brunch', ['nein', 'ja'])
        self.lunch = IndexedMetric('lunch', ['nein', 'ja'])
        self.dinner = IndexedMetric('dinner', ['nein', 'ja'])
        self.student_discount = IndexedMetric('student_discount', ['nein', 'ja'])
        self.wheelchair_accessible = IndexedMetric('wheelchair_accessible', ['nein', 'ja'])

    def export(self, folder):
        for table in self:
            if isinstance(table, IndexedMetric):
                with open(self.output, 'w+', newline='', encoding='UTF-8') as file:
                    writer = csv.DictWriter(file, delimiter=',', 
                    quotechar='"', fieldnames=self._fieldnames())
                    writer.writeheader()
                    for row in transformed_data:
                        writer.writerow(row)
        

class UsersTransformer(IdTransformer):
    def __init__(self, input, output, dbo: Dbo):
        self.dbo = dbo
        super().__init__(input, output)

    def _transform(self, row) -> dict:
        return {
            'user_id': self._id(row['user_id']),
            'gender': vas(row['geschlecht']).default('none').replace('Möchte es lieber nicht sagen', 'none').apply(self.dbo.gender.index).ret(),
            'alcohol_consumption': vas(row['trinkt die Person Alkohol']).default('nein').apply(self.dbo.alcohol_consumption.index).ret(),
            'diet': vas(row['vegetartisch_vegan']).default('keine').apply(self.dbo.diet.index).ret(),
            'beverage_preference_1': vas(row['getränke_präferenz_1']).default('keine').apply(self.dbo.beverage_preference_1.index).ret(),
            'beverage_preference_2': vas(row['getränke_präferenz_2']).default('keine').apply(self.dbo.beverage_preference_2.index).ret(),
            'birthyear': row['alter'],
            'marital_status': vas(row['familienstand']).apply(self.dbo.marital_status.index).ret(),
            'children': vas(row['kinder']).default('nein').replace('0', 'nein').apply(self.dbo.children.index).ret(),
            'student': vas(row['student']).default('nein').apply(self.dbo.student.index).ret(),
            'employee': vas(row['berufstätig']).default('nein').apply(self.dbo.employee.index).ret(),
            'intolerance': val(row['lebensmittel_intoleranzen']).apply(self.dbo.intolerance.index).ret(),
            'religious_preference': vas(row['religioese_praeferenzen']).apply(self.dbo.religious_preference.index).ret()
        }

    def _fieldnames(self) -> list:
        return ['user_id', 'gender', 'alcohol_consumption', 
            'diet', 'beverage_preference_1', 'beverage_preference_2', 
            'birthyear', 'marital_status', 'children', 'student', 
            'employee', 'intolerance', 'religious_preference']

class RestaurantsTransformer(IdTransformer):
    def __init__(self, input, output, dbo: Dbo):
        self.dbo = dbo
        super().__init__(input, output)

    def _transform(self, row) -> dict:
        return {
            'restaurant_id': self._id(row['restaurant_id'])
        }

    def _fieldnames(self) -> list:
        return ['restaurant_id', 'name', 'smoking_area', 
            'price_category', 'takeaway', 'seats_inside', 
            'seats_outside', 'restaurant_type_1', 'restaurant_type_2', 
            'cuisine_type_1', 'cuisine_type_2', 'cuisine_region_1', 
            'cuisine_region_2', 'vegetarian', 'vegan', 
            'breakfast', 'brunch', 'lunch', 'dinner', 
            'student_discount', 'wheelchair_accessible',]

class RatingsTransformer(Transformer):
    def __init__(self, input, output, user_ids, restaurant_ids):
        self.user_ids = user_ids
        self.restaurant_ids = restaurant_ids
        super().__init__(input, output)

    def _transform(self, row) -> dict:
        return { **{
            'user_id': self.user_ids[row['user_id']],
            'restaurant_id': self.restaurant_ids[row['restaurant_id']]
        }, **self._rename(row, {
            'datum': 'date',
            'rating': 'rating'
        })}

    def _fieldnames(self) -> list:
        return ['user_id', 'restaurant_id', 'date', 'rating']