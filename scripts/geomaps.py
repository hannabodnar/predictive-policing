import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from libpysal import weights
from esda.moran import Moran, Moran_Local
import matplotlib.pyplot as plt

# Load shapefile
boundaries = gpd.read_file('Station_Boundaries/Station_Boundaries.shp')
boundaries = boundaries.to_crs(epsg=4326)
lapd_bounds = boundaries[boundaries['ST_NAME'].str.contains('LAPD')]



# Load data
crime_dataset = pd.read_csv('aggragated_data.csv', sep=',', header=0)
#rand_sample = crime_data.sample(frac=0.001, random_state=42)
coords_df = crime_dataset[['Crime Code', 'LAT', 'LON']]
coords_df = coords_df.rename(columns={'LAT': 'Latitude', 'LON': 'Longitude'})

stations = gpd.read_file('LAPD_Police/LAPD_policestation.shp')
coords_df['geometry'] = coords_df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
crimes_gdf = gpd.GeoDataFrame(coords_df, geometry='geometry', crs={'init': 'epsg:4326'})
crimes_gdf = crimes_gdf.to_crs(epsg=4326)
stations = stations.to_crs(epsg=4326)


nearest_station_name = []

for idx, crime in crimes_gdf.iterrows():
    nearest_station = min(stations.iterrows(), key=lambda x: x[1]['geometry'].distance(crime.geometry))
    nearest_station_name.append(nearest_station[1]['DIVISION'])

# Assign the nearest police station names to a new column in crime_data
crimes_gdf['nearest_police_station'] = nearest_station_name

crime_counts = crimes_gdf.groupby('nearest_police_station').size().reset_index(name='crime_count')
crime_counts = pd.DataFrame(crime_counts)
stations = stations.rename(columns={'DIVISION': 'nearest_police_station'})
merged_counts = stations.merge(crime_counts, on='nearest_police_station')
merged_counts = merged_counts.drop(columns=['LOCATION', 'PREC'])


knn_w = weights.KNN.from_dataframe(merged_counts, k=3)
moran = Moran(merged_counts['crime_count'], knn_w)
moran_local = Moran_Local(merged_counts['crime_count'], knn_w)

local_moran_vals = moran_local.Is
p_vals = moran_local.p_sim
crime_count = merged_counts['crime_count']
sig_lev = 0.05
signif_clust = [a for (a, b) in zip(merged_counts['nearest_police_station'].values, merged_counts['crime_count'].values) if b in crime_count[p_vals < sig_lev].values]
signif_div = ['LAPD West Los Angeles Division', 'LAPD Wilshire Division', 'LAPD Hollywood Division', 'LAPD Topanga Division']
high_div = lapd_bounds[lapd_bounds['ST_NAME'].isin(signif_div)]

fig, ax = plt.subplots(figsize=(10, 10))
lapd_bounds.plot(ax=ax, color='lightgrey', edgecolor='black', label='P-Value >= 0.05')
high_div.plot(ax=ax, color='red', label='P-Value < 0.05')
for idx, row in high_div.iterrows():
    ax.annotate(row['ST_NAME'], (row.geometry.centroid.x, row.geometry.centroid.y),
                color='black', fontsize=12, ha='center', va='center')


plt.title("LA Districts with Statistically Significant Moran's I Value")
plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), fontsize='large')
plt.savefig('LAPD_Police/LAPD_police_stations.png')
plt.show()


# Plot Moran's Scatterplot
fig, ax = plt.subplots(figsize=(10, 6))
plt.scatter(merged_counts['crime_count'].values, moran_local.Is, alpha=0.5, color='blue')  # Plot scatterplot
plt.axhline(0, color='red', linestyle='--', linewidth=1, label='No Spatial Autocorrelation')  # Add horizontal line at y=0
plt.axvline(merged_counts['crime_count'].mean(), color='green', linestyle='--', linewidth=1, label='Mean Crime Count')  # Add vertical line at mean value
# Add legend
plt.legend()

# Add explanation for line y=0
#plt.text(0.5, -0.05, 'No Spatial Autocorrelation', color='red', transform=ax.transAxes)

# Label Moran Local value with police station name
for i, txt in enumerate(merged_counts['nearest_police_station']):
    plt.annotate(txt, (merged_counts['crime_count'].values[i], moran_local.Is[i]))

plt.title("Moran's Scatterplot")
plt.xlabel('Crime Counts')
plt.ylabel("Moran's I Local")
plt.grid(True)
#plt.savefig('Moran_scatt.png')
#plt.show()
#print(crimes_gdf)

















