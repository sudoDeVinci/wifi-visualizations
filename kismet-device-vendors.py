import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/processing/sumMacVendors.csv", delimiter=";")

grouped = df.groupby('name')
vendorCount = grouped['name'].count().reset_index(name ='count')

# move all MACs with only one device to "other"
otherRows = vendorCount[vendorCount['count'] <= 1]

# remove all rows with only one device
vendorCountWithoutOthers = vendorCount.drop(otherRows.index)

# add "other" row to dataframe
vendorCountWithoutOthers.loc[len(vendorCountWithoutOthers)] = {'name': 'other devices', 'count': otherRows.count()['count']}

# create the pie chart
plt.figure(figsize=(10, 8))
explode = (0.1, 0, 0, 0, 0.2, 0, 0.3, 0.2, 0.15)
plt.pie(vendorCountWithoutOthers['count'], labels=vendorCountWithoutOthers['name'], startangle=140, explode=explode)
plt.legend(vendorCountWithoutOthers['name'], loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Device vendors (Bluetooth and WiFi)')
plt.axis('equal')

# show the pie chart
plt.show()