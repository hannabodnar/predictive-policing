import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns

data = pd.read_csv('cleaned_data.csv')

# Create table with amount of crimes commited for each crime type
crimes = data.groupby('Crime Desc').size().reset_index(name='Count')
crimes_df = pd.DataFrame(crimes)
crimes_df = crimes_df.sort_values(by='Count', ascending=False)
crimes_df.reset_index(drop=True, inplace=True)
full_table = tabulate(crimes_df, headers='keys', tablefmt='latex_longtable')
with open('crime_counts_table.tex', 'w') as f:
    f.write(full_table)

# first 15 crimes
sub_df = crimes_df[:15]
sub_table = tabulate(sub_df, headers='keys', tablefmt='latex_longtable')
with open('crime_counts_sub.tex', 'w') as f:
    f.write(sub_table)

# Find Male vs Female Victim Proportion
vict_sex = data.groupby('Vict Sex').size().reset_index(name='Count')
vict_sex_df = pd.DataFrame(vict_sex)
vict_sex_df['Prop'] = vict_sex_df['Count'].apply(lambda x: x/sum(vict_sex_df['Count'] / 100))
labels = vict_sex_df['Vict Sex'].values
sizes = vict_sex_df['Prop'].values

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.2f%%', colors=['magenta', 'blue', 'orange'])
plt.title('Victims by Gender')
plt.savefig('vict_gender.png')
plt.show()

# Proportion of Victims by Descent
vict_desc = data.groupby('Vict Descent').size().reset_index(name='Count')
vict_desc_df = pd.DataFrame(vict_desc)
desc = ['Other Asian', 'Black', 'Chinese', 'Cambodian', 'Filipino', 'Guamanian', 'Hispanic/Latin/Mexican', 'American Indian/Alaskan Native', 'Japanese',
        'Korean', 'Laotian', 'Other', 'Pacific Islander', 'Samoan', 'Hawaiian', 'Vietnamese', 'White', 'Unknown', 'Asian Indian']
vict_desc_df['Victim Descent'] = desc

plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Count', y='Victim Descent', data=vict_desc_df, hue='Victim Descent')
for i in ax.containers:
    ax.bar_label(i, padding=2)
plt.subplots_adjust(left=0.27, right=0.95)
plt.title('Number of Crimes Committed by Victim Descent')
plt.savefig('vict_desc.png')
plt.show()

# Victims by Age
vict_age = data[['Crime Desc', 'Vict Age']].copy()
age_ranges = [(0, 0), (1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 80), (81, 120)]
# Function to categorize age
def categorize_age(age):
    for start, end in age_ranges:
        if start <= age <= end:
            return f'{start}-{end}'

# Add a new column for age range category
vict_age['Age Range'] = vict_age['Vict Age'].apply(categorize_age)
vict_age_df = vict_age.groupby('Age Range')['Crime Desc'].count().reset_index()
vict_age_df = pd.DataFrame(vict_age_df)
vict_age_df['Prop'] = vict_age_df['Crime Desc'].apply(lambda x: x/sum(vict_age_df['Crime Desc'] / 100))

cmap = plt.get_cmap('magma')
colors = cmap(np.linspace(0.3, 1.0, len(vict_age_df)))
fig, ax = plt.subplots()
ax.pie(vict_age_df['Prop'], autopct='%1.2f%%', colors=colors, startangle=140, pctdistance=0.5)
plt.legend(vict_age_df['Age Range'], loc='center right', bbox_to_anchor=(1.3, 0.5))
plt.title('Victim Age Distribution')
plt.subplots_adjust(right=0.85, left=0.15)
plt.savefig('vict_age.png')
plt.show()
