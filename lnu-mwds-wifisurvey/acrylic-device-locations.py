import pandas as pd
import folium
import matplotlib.pyplot as plt
import math

df = pd.read_csv('data/in/acrylic-csv/Report-Mapping-building-M-English.csv', delimiter=";")

df2 = df.drop(columns=['Accuracy', 'Altitude', 'SSIDConnectedTo'])

def addMarker(data, map):
    popuptext = "SSID: {} <br> MAC: {} <br> Channel: {}".format(data["SSID"], data["MacAddress"], data["Chan"])
    folium.Marker(location=[data["meanLat"], data["meanLon"]], icon=folium.Icon(icon="wifi", prefix="fa"), popup=popuptext).add_to(map)
    
def generateMapForSSID(df):
    map = folium.Map(location=[56.853997, 14.832758], zoom_start=19)
    df.apply(addMarker, args=[map], axis=1)
    return map

def getMacMean(mac, locationDF):
    rowsWithMac = locationDF[locationDF["MacAddress"] == mac]
    latMean = rowsWithMac["Latitude"].mean()
    lonMean = rowsWithMac["Logitude"].mean()
    return [latMean, lonMean]


# get mean device location from all measurements
uniqueMacVendors = df2[["MacAddress", "Vendor"]].drop_duplicates()
uniqueMacVendors[['meanLat', 'meanLon']] = uniqueMacVendors.apply(lambda row: pd.Series(getMacMean(row["MacAddress"], df2)), axis=1)

# add WiFi details to devices
ssidDetails = df2[["MacAddress", "SSID", "Chan"]].drop_duplicates()
uniqueMacWithWiFi = uniqueMacVendors.merge(ssidDetails, on="MacAddress", how="left")

# plot map
map = generateMapForSSID(uniqueMacWithWiFi)
map.save('data/out/acrylic-device-location.html')