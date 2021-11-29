
from transformer.transformer import IdTransformer, Transformer


class UsersTransformer(IdTransformer):
    def _transform(self, row) -> dict:
        return {
            'user_id': self._id(row['user_id'])
        }

    def _fieldnames() -> list:
        return ['user_id']

class RestaurantsTransformer(IdTransformer):
    def _transform(self, row) -> dict:
        return {
            'restaurant_id': self._id(row['restaurant_id'])
        }

    def _fieldnames() -> list:
        return ['restaurant_id']

class RatingsTransformer(Transformer):
    def __init__(self, input, output, user_ids, restaurant_ids):
        self.user_ids = user_ids
        self.restaurant_ids = restaurant_ids
        super().__init__(input, output)

    def _transform(self, row) -> dict:
        return {
            'user_id': self.user_ids[row['user_id']],
            'restaurant_id': self.user_ids[row['restaurant_id']],
            'date': row['date'],
            'rating': row['rating']
        }

    def _fieldnames() -> list:
        return ['user_id', 'restaurant_id', 'date', 'rating']