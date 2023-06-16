import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import img_tiles
from cartopy.io.img_tiles import OSM

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib_scalebar.scalebar import ScaleBar
import cartopy_zebra_frame as zebra

import matplotlib.path as mpath
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

#latitud = -9.56
#longitud = -73.60


latitud =-0.83
longitud = -79.54

#latitud = -1.52
#longitud = -80.99


margin = 0.50
inset_margin=5
zoom = 9


# Crear los radios de los círculos y la lista de opacidades
radios = [0.01, 0.03, 0.05, 0.07, 0.09]
opacidades = [0.7, 0.6, 0.5, 0.4, 0.3]
colors = ['red', 'red','red','orange','orange']


class MapboxTiles(OSM):
    def _image_url(self, tile):
        
        x, y, z = tile
        url = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{}/{}/{}?access_token={}'.format(z, x, y, mapbox_access_token)
        return url





# Define your custom tile server
class CustomTiles(img_tiles.OSM):
    def _image_url(self, tile):
        x, y, z = tile
        y = 2**z - y - 1 
        url = f'http://localhost:5000/tiles/{z}/{x}/{y}.png'  # Change the url as needed
        return url

# Create the custom tiles
#tiles = CustomTiles() #4.8 segundos
tiles = img_tiles.GoogleTiles(style="street",cache=True) #6 a 4.9 segundos
#tiles = img_tiles.OSM() #7 a 5 segundos
#tiles = MapboxTiles() #7segundos a 5

tiles_inset = tiles
#tiles_inset = CustomTiles() #4.8 segundos

# Create the map and add the custom tiles
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())  # Use Plate Carrée projection
ax.set_extent([longitud - margin, longitud + margin, latitud - margin, latitud + margin])

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)


ax.add_image(tiles, zoom, interpolation='spline36', regrid_shape=1000)
ax.set_xticks([longitud- margin/2,longitud, longitud+margin/2], crs=ccrs.PlateCarree() )
ax.set_yticks([latitud- margin/2,latitud, latitud+margin/2], crs=ccrs.PlateCarree() )
ax.tick_params(axis='both', direction='in', which='both')


# Add the circles
for i, radio in enumerate(radios):
    circle = Circle((longitud, latitud), radius=radio, 
    facecolor='none',
    alpha=opacidades[i], 
    edgecolor=colors[i], 
    transform=ccrs.PlateCarree())
    ax.add_patch(circle)


# Create the inset map and add the custom tiles

inset_extent = [longitud-inset_margin, longitud+inset_margin, latitud-inset_margin, latitud+inset_margin]
inset_ax = fig.add_axes([0.125, 0.125, 0.25, 0.25], projection=ccrs.PlateCarree())  # Use Plate Carrée projection
inset_ax.set_extent(inset_extent)
inset_ax.add_image(tiles_inset, 5, interpolation='spline36', regrid_shape=1000)

'''Generar el ma con cfeatures demora 5 segundos'''
#inset_ax.coastlines()
#inset_ax.add_feature(cfeature.BORDERS)
#inset_ax.add_feature(cfeature.OCEAN)
inset_ax.plot(longitud, latitud, marker='+', color='red', markersize=10, transform=ccrs.PlateCarree())




up_text = "ID: igepn2016hnmu - Revisado \n 2016-04-16 18:58 Hora local \nMagnitude: 7.5"
down_text = ""


#ax.set_title(f"{up_text}")

 
ax.text(x=0.95, y=0.95, s=f"{up_text}", size=13, ha='right', va='top', transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=2))




zebra.add_zebra_frame(ax,crs=ccrs.PlateCarree())

# Add the logo
logo_img = plt.imread("./logo_igepn.png")

#logo_extent = (0,0,0.25,0.25)
#ax.imshow(logo_img, origin='upper', extent=logo_extent, transform=ccrs.PlateCarree())
#logo_extent = (longitud, longitud+10, latitud, latitud+10)

logo_extent = (longitud + margin * 0.7, longitud + margin, latitud + margin * 0.7, latitud + margin)
ax.imshow(logo_img, origin='lower', extent=logo_extent, transform=ccrs.PlateCarree())


# Load the image
logo_img = plt.imread('./logo_igepn.png')

# Create an axes in the figure coordinates with the specified position and size.
logo_axes = fig.add_axes([0.125, 0.70, 0.25, 0.25])  # adjust as needed

# Display the image in these axes
logo_axes.imshow(logo_img)
logo_axes.axis('off')  # hide the axes



# Add a scale bar
#scalebar = ScaleBar(1, "km", length_fraction=0.25, location='lower right')
#scalebar = ScaleBar(1,"km")
#ax.add_artist(scalebar)

# Show the map
#plt.show()
plt.savefig('./test.png')