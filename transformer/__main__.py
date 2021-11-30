
from transformer.project import Dbo, RatingsTransformer, RestaurantsTransformer, UsersTransformer


def run_default_transformer(users_path, restaurants_path, ratings_path):
    dbo = Dbo()

    users_transformer = UsersTransformer(users_path, '.\\output\\user_features.csv', dbo=dbo)
    restaurants_transformer = RestaurantsTransformer(restaurants_path, '.\\output\\restaurant_features.csv', dbo=dbo)

    users_transformer.transform()
    print('Transformed user_features to .\\output\\user_features.csv')
    restaurants_transformer.transform()
    print('Transformed user_features to .\\output\\restaurant_features.csv')

    ratings_transformer = RatingsTransformer(ratings_path, '.\\output\\ratings.csv',
    user_ids=users_transformer.ids, restaurant_ids=restaurants_transformer.ids)
    
    ratings_transformer.transform()
    print('Transformed user_features to .\\output\\ratings.csv')

if __name__ == '__main__':
    run_default_transformer(
        users_path='.\\input\\user_features.csv',
        restaurants_path='.\\input\\restaurant_features.csv',
        ratings_path='.\\input\\ratings.csv'
    )
