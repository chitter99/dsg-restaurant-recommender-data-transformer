import numpy as np
import pandas as pd

from os.path import join

replace_matrix = {
    # boollike
    'Ja': True,
    'Nein': False,
    
    # NaN
    'Keine': np.NaN,
    
    # categoy gender
    'Männlich': 'male',
    'Weiblich': 'female',
    'Nicht-Binär': 'non-binary',

    # category diet
    'Pescetarier': 'pescetarian',
    'vegetarisch': 'vegetarian',

    # categoy beverage_preference
    'Alkohol': 'alcohol',
    'Alkoholfrei': 'non-alcoholic',
    'Bier': 'beer',
    'Cocktails': 'cocktails',
    'Spirituosen': 'spirits',
    'Limonade': 'lemonade',
    'Tee': 'tea',
    'Kaffee': 'coffe',
    'Wasser': 'water',
    'Fruchtsaft': 'juice',
    'Wein': 'wine',

    # categoy marital_status
    'Ledig': 'single',
    'Verheiratet': 'married',
    'Zusammenlebend': 'cohabit',
    'geschieden': 'divorced',
    'verwitwet': 'widowed'
}

def transform_user_features(users: pd.DataFrame) -> pd.DataFrame:
    # drop not needed columns
    users = users.drop(columns=['team_name', 'plz', 'beruf_bezeichnung', 'beruf_branche'])

    # rename columns to keep english name consistency
    users = users.rename(columns={
        'user_id': 'old_user_id',
        'geschlecht': 'gender',
        'trinkt die Person Alkohol': 'alcohol_consumption',
        'vegetartisch_vegan': 'diet',
        'getränke_präferenz_1': 'beverage_preference_1',
        'getränke_präferenz_2': 'beverage_preference_2',
        'alter': 'birthyear',
        'familienstand': 'marital_status',
        'kinder': 'children',
        'berufstätig': 'employee',
        'religioese_praeferenzen': 'religious_preference'
    })
    users.index = users.index.rename('user_id')

    users = users.replace(replace_matrix)

    # convert boolean like strings
    #users['children'] = users['children'].replace(boollike)
    #users['alcohol_consumption'] = users['alcohol_consumption'].replace(boollike)
    #users['student'] = users['student'].replace(boollike)
    #users['employee'] = users['employee'].replace(boollike)

    # feature engineering intolerances from lebensmittel_intoleranzen attribute
    users['lebensmittel_intoleranzen'] = users['lebensmittel_intoleranzen'].astype('string')
    users['intolerance_gluten'] = users['lebensmittel_intoleranzen'].transform(lambda x: not pd.isna(x) and 'Gluten' in x)
    users['intolerance_lactose'] = users['lebensmittel_intoleranzen'].transform(lambda x: not pd.isna(x) and 'Laktoseintoleranz' in x)
    users = users.drop(columns=['lebensmittel_intoleranzen'])

    # update column types
    users = users.astype({
        'gender': 'category',
        'alcohol_consumption': 'bool',
        'diet': 'category',
        'beverage_preference_1': 'category',
        'beverage_preference_2': 'category',
        'marital_status': 'category',
        'children': 'bool',
        'student': 'bool',
        'employee': 'bool',
        'religious_preference': 'category',
        'intolerance_gluten': 'bool',
        'intolerance_lactose': 'bool'
    })
    users['birthyear'] = pd.to_numeric(users['birthyear'], errors='coerce')
    
    return users

def transform_restaurant_features(restaurants: pd.DataFrame) -> pd.DataFrame:
    return restaurants

def transform_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    # drop not needed columns
    ratings = ratings.drop(columns=['team_name', 'datum'])

    # rename index column
    ratings.index = ratings.index.rename('rating_id')

    # update column types
    ratings['rating'] = pd.to_numeric(ratings['rating'])

    return ratings

def main(input='.\\input', output='.\\output'):
    print('               __')
    print('              / _)')
    print('     _.----._/ /')
    print('    /         /')
    print(' __/ (  | (  |')
    print('/__.-\'|_|--|_|')
    print('')
    print('')
    print('super cool restaurant recommender transformer')
    print('')
    print('input=\'{}\''.format(input))
    print('output=\'{}\''.format(output))
    print('')
    print('$ transforming sets')

    users = pd.read_csv(join(input, 'user_features.csv'))
    users = transform_user_features(users)
    print('$ transformed -> {} user features'.format(len(users)))

    restaurants = pd.read_csv(join(input, 'restaurant_features.csv'))
    restaurants = transform_restaurant_features(restaurants)
    print('$ transformed -> {} restaurant features'.format(len(restaurants)))

    ratings = pd.read_csv(join(input, 'ratings.csv'))
    ratings = transform_ratings(ratings)
    print('$ transformed -> {} ratings'.format(len(ratings)))

    print('$ linked new foreign keys')

    users.to_csv(join(output, 'user_features.csv'))
    restaurants.to_csv(join(output, 'restaurant_features.csv'))
    ratings.to_csv(join(output, 'ratings.csv'))
    print('$ exported sets')

    print('')
    print('Done, good night!')

    #print(users.to_markdown())

if __name__ == '__main__':
    main()
