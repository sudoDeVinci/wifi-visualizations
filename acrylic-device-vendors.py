import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/in/acrylic-csv/Report-Mapping-building-M-English.csv', delimiter=";")

df2 = df.drop(columns=['Accuracy', 'Altitude', 'SSIDConnectedTo'])


uniqueMacVendors = df2[["MacAddress", "Vendor"]].drop_duplicates()

grouped = uniqueMacVendors.groupby('Vendor')
vendorCount = grouped['Vendor'].count().reset_index(name ='count')

# move all MACs with only one device to "other"
otherRows = vendorCount[vendorCount['count'] <= 1]

# remove all rows with only one device
vendorCountWithoutOthers = vendorCount.drop(otherRows.index)

# add "other" row to dataframe
vendorCountWithoutOthers.loc[len(vendorCountWithoutOthers)] = {'Vendor': 'other devices', 'count': otherRows.count()['count']}

# create the pie chart
plt.figure(figsize=(10, 8))

explode = (0.1, 0, 0, 0, 0.2, 0, 0.3, 0.2, 0.15)
plt.pie(vendorCountWithoutOthers['count'], labels=vendorCountWithoutOthers['Vendor'], startangle=140) # explode=explode
plt.legend(vendorCountWithoutOthers['Vendor'], loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Device vendors (Bluetooth and WiFi)')
plt.axis('equal')

# show pie chart
plt.show()