import pandas as pd
from tabulate import tabulate

# Load data
data = pd.read_csv('cleaned_data.csv')

# Define Broad Crime Categories
broad_cats = {
    'Vehicle - Stolen': ['vehicle - stolen', 'bike', 'boat', 'vehicle - attempt stolen'],
    'Battery': ['battery'],
    'Burglary': ['burglary'],
    'Robbery': ['robbery'],
    'Assault with Deadly Weapon': ['assault with deadly weapon'],
    'Simple Assault': ['intimate partner - simple assault', 'simple assault'],
    'Other Assault': ['other assault'],
    'Aggravated Assault': ['aggravated assault'],
    'Theft of Identity': ['theft of identity'],
    'Theft from Vehicle': ['theft from motor vehicle', 'theft from motor'],
    'Shoplifting': ['shoplifting'],
    'Bunco': ['bunco'],
    'Grand Theft': ['grand theft'],
    'Petty Theft': ['petty theft', 'theft plain', 'theft from person', 'theft, person', 'petty'],
    'Vandalism': ['vandalism'],
    'Sexual Assault': ['sexual assault', 'rape', 'sodomy', 'penetration', 'oral', 'incest'],
    'Fraud': ['fraud', 'theft of services', 'counterfeit'],
    'Lewd Conduct': ['lewd conduct', 'peeping tom', 'indecent exposure', 'letters, lewd', 'lewd/lascivious'],
    'Arson': ['arson'],
    'Trespassing': ['trespassing'],
    'Criminal Threats - No Weapons': ['criminal threats'],
    'Brandish Weapon': ['brandish weapon', 'replica firearms', 'weapons possession']
}

df = pd.DataFrame(data[['Crime Desc', 'Crime Code']])

# Function to map specific crimes to broad categories
def map_to_broad_category(crime):
    for broad_category, specific_crimes in broad_cats.items():
        for specific_crime in specific_crimes:
            if specific_crime.lower() in crime.lower():
                return broad_category
    return 'Other'  # Default category if no match is found

# Create a new column 'broad_crime_type' based on the mapping
df['broad_crime_type'] = df['Crime Desc'].apply(map_to_broad_category)
agg_df = df.groupby('broad_crime_type')['Crime Code'].first().reset_index()
updated_df = pd.merge(df, agg_df, on='broad_crime_type', how='left')

unique_combinations = df[['Crime Desc', 'broad_crime_type']].drop_duplicates()
unique_combinations.reset_index(drop=True, inplace=True)

# Create LaTex Table
crime_types = tabulate(unique_combinations, headers='keys', tablefmt='latex')
with open('crime_types.tex', 'w') as f:
    f.write(crime_types)

data['Crime Type'] = df['broad_crime_type']
data = data.drop(columns=['Crime Desc', 'Crime Code'])
data['Crime Code'] = updated_df['Crime Code_y']



broad_premise = {
    'Street': ['street'],
    "Multi-Unit Dwelling (Apt, Duplex, etc)": ["multi-unit dwelling"],
    'Sidewalk': ['sidewalk'],
    'Driveway': ['driveway'],
    'Restaurant/Fast Food': ['restaurant/fast food'],
    'Single Family Dwelling': ['single-family dwelling'],
    'Garage/Carport': ['garage/carport'],
    'Transportation Station': ['stop', 'station', 'MTA -'],
    'Vehicle': ['vehicle, passenger', 'train', 'bus', 'truck', 'aircraft', 'tram'],
    'Electronics Store': ['electronics', 'cell phone', 'computer', 'tv'],
    'Bank/Finance': ['bank', 'check', 'atm', 'savings', 'credit'],
    'Entertainment Club': ['bar', 'club'],
    'Sports Facility': ['hockey', 'sports', 'stadium', 'gym', 'coliseum', 'courts', 'bowling', 'arcade', 'golf', 'racing'],
    'Place of Worship': ['church', 'temple', 'synagogue', 'mosque', 'place of worship'],
    'Medical/Dental Clinic': ['medical', 'dental', 'clinic', 'hospital'],
    'School/University': ['school', 'university'],
    'Department Stores': ['clothing', 'furniture', 'DIY', 'department', 'hardware', 'supplu', 'jewelry'],
    'Park/Museum': ['park', 'museum'],
    'Parking Lot': ['parking', ' storage lot', 'valet', 'mini', 'storage'],
    'Supermarket': ['supermarket', 'grocery', 'market', 'membership', 'liquor'],
    'Other Business': ['business', 'tattoo', 'nail', 'beauty', 'massage', 'shop', 'wash', 'drug', 'center', 'plant', 'auto', 'studio', 'service', 'mall', 'gas', 'post', 'laundromat', 'motel'],
    'Other Residence': ['other residence', 'home', 'housing', 'shelter', 'frat', 'vacation', 'mobile', 'hospice', 'high-rise', 'room'],
    'Public Area': ['tracks', 'tunnel', 'public', 'elevator', 'freeway', 'theatre', 'overcrossing', 'monument', 'yard', 'beach', 'stairwell', 'bridge', 'outside', 'mailbox', 'balcony', 'alley'],
    'Government Facility': ['government', 'police', 'fire', 'library', 'jail']
}

new_df = pd.DataFrame(data[['Premis Code', 'Premis Desc']])


def map_to_category(loc):
    for broad_prem, specific_locs in broad_premise.items():
        for specific_loc in specific_locs:
            if specific_loc.lower() in loc.lower():
                return broad_prem
    return 'Other'  # Default category if no match is found

new_df['broad premise'] = new_df['Premis Desc'].apply(map_to_category)
agg_df2 = new_df.groupby('broad premise')['Premis Code'].first().reset_index()
updated_new_df = pd.merge(new_df, agg_df2, on='broad premise', how='left')

data['Premise Desc'] = new_df['broad premise']
data['Premise Code'] = updated_new_df['Premis Code_y']
data = data.drop(columns=['Premis Code', 'Premis Desc'])

data.to_csv('aggragated_data.csv', index=False)
