import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt

latitud = 0.96
longitud = -79.62



# Agregar la imagen del mapa base de OpenStreetMap
tiles = cimgt.OSM()
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1, projection=tiles.crs)
ax.add_image(tiles, 10)

# Agregar el marcador en la ubicación especificada
ax.plot(longitud, latitud, 'o', color='green', markersize=10, markerfacecolor='none', transform=ccrs.PlateCarree())

# Establecer los límites del mapa
ax.set_extent([longitud-0.5, longitud +0.5 , latitud -0.5, latitud +0.5 ], crs=ccrs.PlateCarree())

plt.show()

