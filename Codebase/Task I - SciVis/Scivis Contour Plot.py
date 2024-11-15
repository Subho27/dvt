import numpy as np
import pandas as pd
import imageio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import matplotlib.dates as mdates
import xarray as xr

nc_files = ['./_DATASET/bi_2023.nc', './_DATASET/erc_2023.nc',
           './_DATASET/etr_2023.nc', './_DATASET/fm1000_2023.nc',
           './_DATASET/fm100_2023.nc', './_DATASET/fm10_2023.nc',
           './_DATASET/fm1_2023.nc', './_DATASET/pet_2023.nc',
           './_DATASET/pr_2023.nc', './_DATASET/rmax_2023.nc',
           './_DATASET/rmin_2023.nc', './_DATASET/sph_2023.nc',
           './_DATASET/srad_2023.nc', './_DATASET/tmmn_2023.nc',
           './_DATASET/tmmx_2023.nc', './_DATASET/vpd_2023.nc']

nc_data = ['burning_index_g', 'energy_release_component-g', 'potential_evapotranspiration',
          'dead_fuel_moisture_1000hr', 'dead_fuel_moisture_100hr', 'dead_fuel_moisture_10hr',
          'dead_fuel_moisture_1hr', 'potential_evapotranspiration', 'precipitation_amount', 
          'relative_humidity', 'relative_humidity', 'specific_humidity', 
          'surface_downwelling_shortwave_flux_in_air', 'air_temperature', 'air_temperature',
          'mean_vapor_pressure_deficit']

label_names = ['Burning Index', 'Energy Release Component', 'Reference alfalfa evaportranspiration',
              '1000-hour dead fuel moisture', '100-hour dead fuel moisture', '10-hour dead fuel moisture', 
              '1-hour dead fuel moisture', 'Reference grass evapotranspiration', 'Precipitation',
              'Maximum Near-Surface Relative Humidity', 'Minimum Near-Surface Relative Humidity', 
              'Near-Surface Specific Humidity', 'Surface Downwelling Solar Radiation', 
              'Minimum Near-Surface Air Temperature', 'Maximum Near-Surface Air Temperature',
              'Mean Vapor Pressure Deficit']

result_ms_filenames = [
    f"./animation/contour_plots/marching_squares/{name.lower().replace('-', '_').replace(' ', '_')}_animation.gif" 
    for name in label_names
]

result_cf_filenames = [
    f"./animation/contour_plots/contour_fill/{name.lower().replace('-', '_').replace(' ', '_')}_animation.gif" 
    for name in label_names
]

# Define date range
date_range = pd.date_range(start="2023-08-01", end="2023-10-31", periods=10)
dates = [str(date.date()) for date in date_range]


# Creating animation
for index, nc_file in enumerate(nc_files):

    # Get the dataset & convert it into dataframe 
    nc_dataset = xr.open_dataset(nc_file)
    nc_df = nc_dataset.to_dataframe().reset_index()
    nc_df = nc_df[(nc_df['day'] >= '2023-08-01') & (nc_df['day'] <= '2023-10-31')]
    nc_df = nc_df.reset_index(drop=True)
    nc_df = nc_df.dropna(subset=[nc_data[index]])
    
    # Define contour levels
    levels = np.linspace(nc_df[nc_data[index]].min(), nc_df[nc_data[index]].max(), 10)

    # Animation Marching Squares
    image_files_ms = []
    
    for date in dates:
        # Filter data for the specific date
        df_date = nc_df[nc_df['day'] == date]  
        
        # Create a 2D grid for contour plot
        df_pivot = df_date.pivot(index='lat', columns='lon', values=nc_data[index])
        lon = df_pivot.columns.values
        lat = df_pivot.index.values
        pivot_values = df_pivot.values
    
        # Plot for the specific date
        plt.figure(figsize=(10, 6))
        plt.contour(lon, lat, pivot_values, levels=levels, cmap='inferno')
        plt.colorbar(label=label_names[index])
        plt.title(f"{label_names[index]} Contour - {date}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
    
        # Save plot as an image file
        file_name = f"plot_{date}.png"
        plt.savefig(f"./dumps/{file_name}")
        image_files_ms.append(file_name)
        plt.close()
    
    # Generate GIF using imageio
    with imageio.get_writer(result_ms_filenames[index], mode='I', duration=2.5) as writer:
        for file_name in image_files_ms:
            image = imageio.imread(f"./dumps/{file_name}")
            writer.append_data(image)

    # Animation Contour Fill
    image_files_cf = []

    for date in dates:
        # Filter data for the specific date
        df_date = nc_df[nc_df['day'] == date]
        
        # Create a 2D grid for contour plot
        df_pivot = df_date.pivot(index='lat', columns='lon', values=nc_data[index])
        lon = df_pivot.columns.values
        lat = df_pivot.index.values
        pivot_values = df_pivot.values
    
        # Plot for the specific date
        plt.figure(figsize=(10, 6))
        plt.contourf(lon, lat, pivot_values, levels=levels, cmap='inferno')
        plt.colorbar(label=label_names[index])
        plt.title(f"{label_names[index]} Contour - {date}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
    
        # Save plot as an image file
        file_name = f"plot_{date}.png"
        plt.savefig(f"./dumps/{file_name}")
        image_files_cf.append(file_name)  # Add file to the list of image files
        plt.close()  # Close the plot to save memory
    
    # Generate GIF using imageio
    with imageio.get_writer(result_cf_filenames[index], mode='I', duration=2.5) as writer:
        for file_name in image_files_cf:
            image = imageio.imread(f"./dumps/{file_name}")
            writer.append_data(image)
