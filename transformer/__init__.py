from main import run_default_transformer

if __name__ == '__main__':
    run_default_transformer(
        users_path='.\\input\\user_features.csv',
        restaurants_path='.\\input\\restaurant_features.csv',
        ratings_path='.\\input\\ratings.csv'
    )
