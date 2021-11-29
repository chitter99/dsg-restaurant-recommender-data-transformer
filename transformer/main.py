
from transformer.project import RatingsTransformer, RestaurantsTransformer, UsersTransformer


def run_default_transformer(users_path, restaurants_path, ratings_path):
    users_transformer = UsersTransformer(users_path, '.\\output\\user_features.csv')
    restaurants_transformer = RestaurantsTransformer(restaurants_path, '.\\output\\restaurant_features.csv')

    users_transformer.transform()
    restaurants_transformer.transform()

    ratings_transformer = RatingsTransformer(ratings_path, '.\\output\\ratings.csv',
        user_ids=users_transformer.ids, restaurant_ids=restaurants_transformer.ids)
    
    ratings_transformer.transform()
