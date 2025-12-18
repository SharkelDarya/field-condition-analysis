import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def load_geojson(geojson_path):
    return gpd.read_file(geojson_path)

def load_raster(tiff_path):
    return rasterio.open(tiff_path)

st.title("Field condition analysis")

geojson_file = 'vector_data/dzialki.geojson'
tiff_file = 'raster_data/True_color.tiff'
tiff_b08_file = 'raster_data/B08.tiff' 
tiff_b04_file = 'raster_data/B04.tiff'  
tiff_b11_file = 'raster_data/B11.tiff'  

gdf = load_geojson(geojson_file)
raster = load_raster(tiff_file)
raster_b08 = load_raster(tiff_b08_file)
raster_b04 = load_raster(tiff_b04_file)
raster_b11 = load_raster(tiff_b11_file)

gdf = gdf.to_crs(epsg=4326)

col1, col2 = st.columns([3, 1])

with col2:
    layer_choice = st.radio("Select layer", ("True Color", "NDVI", "Moisture Index"))

def plot_map(layer_choice):
    fig, ax = plt.subplots(figsize=(10, 10))

    if layer_choice == "True Color":
        img_array = raster.read([1, 2, 3])
        img_array = np.moveaxis(img_array, 0, -1) 

        bounds = raster.bounds
        ax.imshow(img_array, extent=[bounds[0], bounds[2], bounds[1], bounds[3]], origin='upper')

    elif layer_choice == "NDVI":
        nir_array = raster_b08.read(1)
        red_array = raster_b04.read(1)

        # Вычисление NDVI
        ndvi = (nir_array - red_array) / (nir_array + red_array)
        
        norm = mcolors.Normalize(vmin=np.min(ndvi), vmax=np.max(ndvi))
    
        im = ax.imshow(ndvi, cmap='RdYlGn', norm=norm, extent=[raster_b08.bounds[0], raster_b08.bounds[2], raster_b08.bounds[1], raster_b08.bounds[3]], origin='upper')
        
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.7, fraction=0.03, pad=0.04)
        cbar.set_label('NDVI Value')

        ax.set_axis_off()
        ax.set_xticks([]) 
        ax.set_yticks([]) 

        ax.set_title('NDVI Index')

    elif layer_choice == "Moisture Index":
        swir_array = raster_b11.read(1)
        nir_array = raster_b08.read(1)

        moisture_index = (swir_array - nir_array) / (swir_array + nir_array)
        norm = mcolors.Normalize(vmin=np.min(moisture_index), vmax=np.max(moisture_index))
        
        im = ax.imshow(moisture_index, cmap='turbo', norm=norm, extent=[raster_b11.bounds[0], raster_b11.bounds[2], raster_b11.bounds[1], raster_b11.bounds[3]], origin='upper')
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.7, fraction=0.03, pad=0.04)
        cbar.set_label('Moisture Index')
        
        ax.set_title('Moisture Index') 
        
    gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

    ax.set_axis_off() 
    ax.set_xticks([]) 
    ax.set_yticks([])

    ax.set_aspect('auto', adjustable='box')

    return fig

with col1:
    fig = plot_map(layer_choice)
    st.pyplot(fig)
