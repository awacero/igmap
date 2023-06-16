import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from cartopy.io import img_tiles


inset_margin=5
#latitud = 0.96
#longitud = -79.62
latitud = -0.25
longitud = -78.53
#latitud = 36.13
#longitud = 36.01

margin = 0.50

# Create the radii of the circles and the list of opacities
radios = [0.01, 0.03, 0.05, 0.07 ]
opacidades = [0.7, 0.6, 0.5, 0.4]
colors = ['red', 'red','orange','yellow']


# Define your custom tile server
class CustomTiles(img_tiles.OSM):
    def _image_url(self, tile):
        x, y, z = tile
        y = 2**z - y - 1 
        url = f'http://localhost:5000/tiles/{z}/{x}/{y}.png'  # Change the url as needed
        return url

# Create the custom tiles
imagery = CustomTiles()

# Create the main map
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([longitud - margin, longitud + margin, latitud - margin, latitud + margin])

# Add the custom tiles
ax.add_image(imagery, 10)  # Change the number as needed

# Add the concentric circles
for i, radio in enumerate(radios):
    circle = Circle((longitud, latitud), radius=radio, 
    facecolor='none',
    alpha=opacidades[i], 
    edgecolor=colors[i], 
    transform=ccrs.PlateCarree())
    ax.add_patch(circle)

# Show the map
plt.show()
