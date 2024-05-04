import pandas as pd
import folium

# Read the CSV file
df = pd.read_csv('data/in/kismet/kismet-device-locations.csv', delimiter="\t")

# Drop unnecessary columns
df_cleaned = df.drop(columns=['min_lat', 'min_lon', 'max_lat', 'max_lon'])

def create_marker_popup(row):
    # Generate the popup text for the marker
    popup_text = f"Type: {row['type']} <br> MAC: {row['devmac']} <br> Signal Peak: {row['strongest_signal']}"
    return folium.Marker(
        location=[row['meanLat'], row['meanLon']],
        icon=folium.Icon(icon="wifi", prefix="fa"),
        popup=popup_text
    )

def generate_map(df):
    # Create a map centered at specific coordinates
    map_obj = folium.Map(location=[56.853997, 14.832758], zoom_start=19)
    
    # Iterate through each row and add a marker to the map
    for _, row in df.iterrows():
        marker = create_marker_popup(row)
        marker.add_to(map_obj)
    
    return map_obj

def calculate_mean_location(mac, location_df):
    # Get rows with the specified MAC address
    rows_with_mac = location_df[location_df["devmac"] == mac]
    
    # Calculate the mean latitude and longitude
    lat_mean = rows_with_mac["avg_lat"].mean()
    lon_mean = rows_with_mac["avg_lon"].mean()
    
    return [lat_mean, lon_mean]

# Get unique combinations of MAC address and device type
unique_mac_vendors = df_cleaned[["devmac", "phyname"]].drop_duplicates()

# Calculate mean location for each unique MAC address
unique_mac_vendors[['meanLat', 'meanLon']] = unique_mac_vendors.apply(lambda row: pd.Series(calculate_mean_location(row["devmac"], df_cleaned)), axis=1)

# Extract unique combinations of MAC address, device type, and signal strength
ssid_details = df_cleaned[["devmac", "type", "strongest_signal"]].drop_duplicates()
#print(ssid_details)
# Merge the data with WiFi details
unique_mac_with_wifi = unique_mac_vendors.merge(ssid_details, on="devmac", how="left")
print(unique_mac_with_wifi)
# Generate the map and save it as an HTML file
map_obj = generate_map(unique_mac_with_wifi)
map_obj.save('data/out/kismet-device-location.html')
