
#SpaceX launch site loacation
#Launch Sites Locations Analysis with Folium


import folium
import wget
import pandas as pd
import folium
import wget
import pandas as pd
#Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
#Import folium MousePosition plugin
from folium.plugins import MousePosition
#Import folium DivIcon plugin
from folium.features import DivIcon


##If you need to refresh your memory about folium, you may download and refer to this previous folium lab:
##
##Generating Maps with Python
##
##Task 1: Mark all launch sites on a map¶
##First, let's try to add each site's location on a map using site's latitude and longitude coordinates
##
##The following dataset with the name spacex_launch_geo.csv is an augmented dataset with latitude and longitude added for each site.

# Download and read the `spacex_launch_geo.csv`
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)

spacex_df.Lat

#Now, you can take a look at what are the coordinates for each site.

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
#launch_sites_df['Launch Site']
​
launch_sites_df.Lat
#launch_sites_df['Lat'][0]

#We first need to create a folium Map object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
usa_centre = [31.50, -98.35]
site_map = folium.Map(location=usa_centre, zoom_start=4)
site_map

#We could use folium.Circle to add a highlighted circle area with a text label on a specific coordinate. For example,

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=folium.DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)


#Now, let's add a circle for each launch site in data frame launch_sites

#TODO: Create and add folium.Circle and folium.Marker for each launch site on the site map

#Basic manual solution.
# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=4)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label



circle = folium.Circle([launch_sites_df['Lat'][0],launch_sites_df['Long'][0]], radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_sites_df['Launch Site'][0]))
circle1 = folium.Circle([launch_sites_df['Lat'][1],launch_sites_df['Long'][1]], radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_sites_df['Launch Site'][1]))


marker = folium.map.Marker(
    [launch_sites_df['Lat'][0],launch_sites_df['Long'][0]],
    # Create an icon as a text label
    icon=folium.DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_sites_df['Launch Site'][0],
        )
    
    )
marker1 = folium.map.Marker(
    [launch_sites_df['Lat'][1],launch_sites_df['Long'][1]],
    # Create an icon as a text label
    icon=folium.DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_sites_df['Launch Site'][1],
        )
    
    )


site_map.add_child(circle)
site_map.add_child(marker)
site_map.add_child(circle1)
site_map.add_child(marker1)

#--------------------------------

#This is a decent solution

from folium import plugins
# instantiate a feature group for the incidents in the dataframe


# loop through the 100 crimes and add each to the incidents feature group
for lat, lng, lab in zip(launch_sites_df.Lat, launch_sites_df.Long, launch_sites_df['Launch Site']):
    folium.Circle(
        [lat, lng],
        radius=1000, color='#d35400', fill=True, # define how big you want the circle markers to be
        fill_opacity=0.6).add_child(folium.Popup(lab)).add_to(site_map)
    folium.map.Marker([lat, lng], icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % lab, )).add_to(site_map)
site_map
# add incidents to map
#site_map.add_child(launchsites)

##Task 2: Mark the success/failed launches for each site on the map
##Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates. Recall that data frame spacex_df has detailed launch records, and the class column indicates if this launch was successful or not

spacex_df.tail(10)

##Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.
##
##Let's first create a MarkerCluster object

marker_cluster = MarkerCluster()
​
#TODO: Create a new column in launch_sites dataframe called marker_color to store the marker colors based on the class value

# Function to assign color to launch outcome
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)
spacex_df.tail(10)


usa_centre = [31.50, -98.35]
site_map = folium.Map(location=usa_centre, zoom_start=4)

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)


# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    #print(index)
    #print (record['marker_color'])
    marker = folium.Marker(location = [record['Lat'], record['Long']], popup= (record['Launch Site'] +' Lat: ' + str(record['Lat'])+' Long: ' + str(record['Long'])), icon=folium.Icon(color=record['marker_color']) ).add_to(marker_cluster)
    #marker_cluster.add_child(marker)
    #popup= record['Launch Site'] ,
    #icon=folium.Icon(color='white', icon_color=row['marker_color'])
for lat, lng, lab in zip(launch_sites_df.Lat, launch_sites_df.Long, launch_sites_df['Launch Site']):
    folium.Circle(
        [lat, lng],
        radius=55, color='#d35400', fill=True, # define how big you want the circle markers to be
        fill_opacity=0.6).add_child(folium.Popup(lab)).add_to(site_map)
    folium.map.Marker([lat, lng], icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % lab, )).add_to(site_map)
    
site_map

##TASK 3: Calculate the distances between a launch site to its proximities
##Next, we need to explore and analyze the proximities of launch sites.

Let's first add a MousePosition on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
​
site_map.add_child(mouse_position)
site_map

You can calculate the distance between two points on the map based on their Lat and Long values using the following method:

from math import sin, cos, sqrt, atan2, radians
​
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
​
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
​
    dlon = lon2 - lon1
    dlat = lat2 - lat1
​
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
​
    distance = R * c
    return distance


#TODO: Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.

# find coordinate of the closet coastline
coastline_lat = 28.56329  
coastline_long = -80.56798
CCAFS_SLC40_lat = 28.56319718 
CCAFS_SLC40_long =  -80.57682003
distance_coastline = calculate_distance(CCAFS_SLC40_lat, CCAFS_SLC40_long, coastline_lat, coastline_long)
distance_coastline
0.8636622534799093
TODO: After obtained its coordinate, create a folium.Marker to show the distance

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
coastline_coordinate = [coastline_lat, coastline_long]
distance_marker = folium.Marker(
   coastline_coordinate,
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
       )
   )
site_map.add_child(distance_marker)
site_map

##TODO: Draw a PolyLine between a launch site to the selected coastline point

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
points = [(CCAFS_SLC40_lat, CCAFS_SLC40_long), (coastline_lat, coastline_long)]
folium.PolyLine(points, weight=1, color='blue', opacity = 1).add_to(site_map)
​
site_map

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site

#Railway
#Coordinates 
railway_lat = 28.57208  
railway_long = -80.58528
CCAFS_SLC40_lat = 28.56319718 
CCAFS_SLC40_long =  -80.57682003
#Calculating distance
distance_railway = calculate_distance(CCAFS_SLC40_lat, CCAFS_SLC40_long, railway_lat, railway_long)
distance_railway

#Adding marker with distance displayed
railway_coordinate = [railway_lat, railway_long]
distance_marker = folium.Marker(
   railway_coordinate,
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_railway),
       )
   )
site_map.add_child(distance_marker)

# Adding a poly line 
points = [(CCAFS_SLC40_lat, CCAFS_SLC40_long), (railway_lat, railway_long)]
folium.PolyLine(points, weight=1, color='red', opacity = 1).add_to(site_map)


#Display site_map
site_map

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site

#Highway
#Coordinates 
city_lat = 28.56327  
city_long = -80.80711
CCAFS_SLC40_lat = 28.56319718 
CCAFS_SLC40_long =  -80.57682003
#Calculating distance
distance_city = calculate_distance(CCAFS_SLC40_lat, CCAFS_SLC40_long, city_lat, city_long)
distance_city

#Adding marker with distance displayed
city_coordinate = [city_lat, city_long]
distance_marker = folium.Marker(
   city_coordinate,
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_city),
       )
   )
site_map.add_child(distance_marker)

# Adding a poly line 
points = [(CCAFS_SLC40_lat, CCAFS_SLC40_long), (city_lat, city_long)]
folium.PolyLine(points, weight=2, color='orange', opacity = 1).add_to(site_map)


#Display site_map
site_map

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site

#Highway
#Coordinates 
highway_lat = 28.56311  
highway_long = -80.57076
CCAFS_SLC40_lat = 28.56319718 
CCAFS_SLC40_long =  -80.57682003
#Calculating distance
distance_highway = calculate_distance(CCAFS_SLC40_lat, CCAFS_SLC40_long, highway_lat, highway_long)
distance_highway

#Adding marker with distance displayed
highway_coordinate = [highway_lat, highway_long]
distance_marker = folium.Marker(
   highway_coordinate,
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_highway),
       )
   )
site_map.add_child(distance_marker)

# Adding a poly line 
points = [(CCAFS_SLC40_lat, CCAFS_SLC40_long), (highway_lat, highway_long)]
folium.PolyLine(points, weight=1, color='green', opacity = 1).add_to(site_map)


#Display site_map
site_map


