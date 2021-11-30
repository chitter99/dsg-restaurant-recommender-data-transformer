import numpy as np
import pandas as pd

from os.path import join

# consts
boollike = {
    'Ja': True,
    'Nein': False
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

    # replace "Keine" with NaN
    users = users.replace('Keine', np.NaN)

    # convert boolean like strings
    users['children'] = users['children'].replace(boollike)
    users['alcohol_consumption'] = users['alcohol_consumption'].replace(boollike)
    users['student'] = users['student'].replace(boollike)
    users['employee'] = users['employee'].replace(boollike)

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
    pass

def transform_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    pass

def main(input='.\\input', output='.\\output'):
    users = pd.read_csv(join(input, 'user_features.csv'))
    users = transform_user_features(users)
    print(users.to_markdown())

if __name__ == '__main__':
    main()
