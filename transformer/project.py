
from transformer.transformer import IdTransformer, IndexedMetric, Transformer, val, vas

class Dbo:
    def __init__(self) -> None:
        self.gender = IndexedMetric(['none', 'female', 'male', 'non-binary'])
        self.alcohol_consumption = IndexedMetric(['nein', 'ja'])
        self.diet = IndexedMetric(['keine' 'vegetarian', 'vegan', 'pescatarian'])
        self.beverage_preference_1 = IndexedMetric()
        self.beverage_preference_2 = IndexedMetric()
        self.marital_status = IndexedMetric()
        self.children = IndexedMetric(['nein', 'ja'])
        self.student = IndexedMetric(['nein', 'ja'])
        self.employee = IndexedMetric(['nein', 'ja'])
        self.intolerance = IndexedMetric()
        self.religious_preference = IndexedMetric()
        self.smoking_area = IndexedMetric(['nein', 'ja'])
        self.takeaway = IndexedMetric(['nein', 'ja'])
        self.seats_inside = IndexedMetric(['nein', 'ja'])
        self.seats_outside = IndexedMetric(['nein', 'ja'])
        self.restaurant_type_1 = IndexedMetric()
        self.restaurant_type_2 = IndexedMetric()
        self.cuisine_type_1 = IndexedMetric()
        self.cuisine_type_2 = IndexedMetric()
        self.cuisine_region_1 = IndexedMetric()
        self.cuisine_region_2 = IndexedMetric()
        self.vegetarian = IndexedMetric(['nein', 'ja'])
        self.vegen = IndexedMetric(['nein', 'ja'])
        self.vegetarian = IndexedMetric(['nein', 'ja'])
        self.breakfast = IndexedMetric(['nein', 'ja'])
        self.brunch = IndexedMetric(['nein', 'ja'])
        self.lunch = IndexedMetric(['nein', 'ja'])
        self.dinner = IndexedMetric(['nein', 'ja'])
        self.student_discount = IndexedMetric(['nein', 'ja'])
        self.wheelchair_accessible = IndexedMetric(['nein', 'ja'])
        

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