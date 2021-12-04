import numpy as np
import pandas as pd

from typing import Tuple
from os.path import join

from pandas.core import indexing

replace_matrix = {
    # boollike
    'Ja': True,
    'ja': True,
    'Nein': False,
    'nein': False,
    'Weiss nicht': False,
    
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
    'Kaffee': 'coffee',
    'Wasser': 'water',
    'Fruchtsaft': 'juice',
    'Wein': 'wine',

    # categoy marital_status
    'Ledig': 'single',
    'Verheiratet': 'married',
    'Zusammenlebend': 'cohabit',
    'geschieden': 'divorced',
    'verwitwet': 'widowed',

    # category religion
    'Muslimisch': 'muslim',

    # category restaurant_type
    'Bar': 'bar', 
    'Cafe': 'coffee', 
    'Fastfood': 'fastfood',
    'FastFood': 'fastfood', 
    'Pub': 'pub', 
    'Restaurant': 'restaurant',
    'Weinbar': 'winebar',

    # category cuisine_type
    'Burger': 'burger', 
    'Fusion': 'fusion', 
    'Grill': 'bbq',
    'Gutbürgerlich': 'plain',
    'Marktküche': 'market',
    'Noodle': 'noodle',
    'Pizza': 'pizza',
    'Sandwich': 'sandwich',
    'Suppen': 'soup',
    'Sushi': 'sushi',
    'Tapas': 'tapas',

    # category cuisine_region
    'Afrikanisch': 'african', 
    'Afghanisch': 'afghan', 
    'Amerikanisch': 'american', 
    'Asiatisch': 'asian', 
    'Chinesisch': 'chinese', 
    'Europäisch': 'european',
    'Indisch': 'indian', 
    'Italienisch': 'italian', 
    'Japanisch': 'japanese', 
    'Mediterran': 'mediterranean', 
    'Mexikanisch': 'mexican',
    'Orientalisch': 'oriental',
    'Schweizerisch': 'swiss',
    'Spanisch': 'spanish',
    'Thailändisch': 'thai', 
    'Tibetisch': 'tibetan'
}

def transform_user_features(users: pd.DataFrame) -> pd.DataFrame:
    # arrange index to start from 1
    users.index = np.arange(1, users.shape[0] + 1)

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

    # apply replacement matrix
    users = users.replace(replace_matrix)

    # feature engineering intolerances from lebensmittel_intoleranzen attribute
    users['lebensmittel_intoleranzen'] = users['lebensmittel_intoleranzen'].astype('string')
    users['intolerance_gluten'] = users['lebensmittel_intoleranzen'].transform(lambda x: not pd.isna(x) and 'Gluten' in x)
    users['intolerance_lactose'] = users['lebensmittel_intoleranzen'].transform(lambda x: not pd.isna(x) and 'Laktoseintoleranz' in x)
    users = users.drop(columns=['lebensmittel_intoleranzen'])

    # update column types
    users = users.astype({
        'gender': 'category',
        'alcohol_consumption': 'int',
        'diet': 'category',
        'beverage_preference_1': 'category',
        'beverage_preference_2': 'category',
        'marital_status': 'category',
        'children': 'int',
        'student': 'int',
        'employee': 'int',
        'religious_preference': 'category',
        'intolerance_gluten': 'int',
        'intolerance_lactose': 'int'
    })
    users['birthyear'] = pd.to_numeric(users['birthyear'], errors='coerce')
    
    return users

def transform_restaurant_features(restaurants: pd.DataFrame) -> pd.DataFrame:
    # arrange index to start from 1
    restaurants.index = np.arange(1, restaurants.shape[0] + 1)

    # drop now needed columns
    restaurants = restaurants.drop(columns=['team_name', 'osm_node_id', 'breite', 'laenge', 'strasse', 'hausnummer', 'stadt', 'plz', 'website'])

    # rename columns to keep english name consistency
    restaurants = restaurants.rename(columns={
        'restaurant_id': 'old_restaurant_id',
        'raucherbereich_innen': 'smoking_area',
        'preis_kategorie': 'price_category',
        'sitzplätze_innen': 'seats_inside',
        'sitzplätze_aussen': 'seats_outside',
        'restaurant_typ_1': 'restaurant_type_1',
        'restaurant_typ_2': 'restaurant_type_2',
        'vegetarisch': 'vegetarian',
        'frühstück': 'breakfast',
        'mittagessen': 'lunch',
        'abendessen': 'dinner',
        'rabatt_pct': 'student_discount',
        'rollstuhlgaengig': 'wheelchair_accessible'
    })
    restaurants.index = restaurants.index.rename('restaurant_id')

    # apply replacement matrix
    restaurants = restaurants.replace(replace_matrix)

    # update column types
    restaurants = restaurants.astype({
        'name': 'string',
#        'smoking_area': 'int',
#        'price_category': 'int',
#        'takeaway': 'int',
#        'seats_inside': 'int',
#        'seats_outside': 'int',
        'restaurant_type_1': 'category',
        'restaurant_type_2': 'category',
        'cuisine_type_1': 'category',
        'cuisine_type_2': 'category',
        'cuisine_region_1': 'category',
        'cuisine_region_2': 'category',
#        'vegetarian': 'int',
#        'vegan': 'int',
#        'breakfast': 'int',
#        'brunch': 'int',
#        'lunch': 'int',
#        'dinner': 'int',
#        'student_discount': 'int',
#        'wheelchair_accessible': 'int'
    })

    numberics = [
        'smoking_area',
        'price_category',
        'takeaway',
        'seats_inside',
        'seats_outside',
        'vegetarian',
        'vegan',
        'breakfast',
        'brunch',
        'lunch',
        'dinner',
        'student_discount',
        'wheelchair_accessible'
    ]

    for attribute in numberics:
        restaurants[attribute] = pd.to_numeric(restaurants[attribute], errors='coerce', downcast='integer').astype(str).replace('\.0', '', regex=True)

    return restaurants

def transform_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    # arrange index to start from 1
    ratings.index = np.arange(1, ratings.shape[0] + 1)

    # drop not needed columns
    ratings = ratings.drop(columns=['team_name', 'datum'])

    # rename index column
    ratings.index = ratings.index.rename('rating_id')

    # update column types
    ratings['rating'] = pd.to_numeric(ratings['rating'])

    # remove dublicate rows
    ratings = ratings.drop_duplicates()

    return ratings

def transform_foreign_keys(users: pd.DataFrame, restaurants: pd.DataFrame, ratings: pd.DataFrame) -> Tuple:
    # match ratings with new ids
    ratings['user_id'] = ratings['user_id'].transform(lambda x: users.index[users['old_user_id'] == x].tolist()[0])
    ratings['restaurant_id'] = ratings['restaurant_id'].transform(lambda x: restaurants.index[restaurants['old_restaurant_id'] == x].tolist()[0])
    
    # remove old ids
    users = users.drop(columns=['old_user_id'])
    restaurants = restaurants.drop(columns=['old_restaurant_id'])

    return (users, restaurants, ratings)

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

    (users, restaurants, ratings) = transform_foreign_keys(users, restaurants, ratings)
    print('$ linked new foreign keys')

    users.to_csv(join(output, 'user_features.csv'))
    restaurants.to_csv(join(output, 'restaurant_features.csv'))
    ratings.to_csv(join(output, 'ratings.csv'), index=False)
    print('$ exported sets')

    print('')
    print('Done, good night!')

    #print(users.to_markdown())

if __name__ == '__main__':
    main()
