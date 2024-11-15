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

# Get the dataset & convert it into dataframe 
th_data = xr.open_dataset('./_DATASET/th_2023.nc')
vs_data = xr.open_dataset('./_DATASET/vs_2023.nc')

# Define date range
date_range = pd.date_range(start="2023-08-01", end="2023-10-31", periods=10)
dates = [str(date.date()) for date in date_range]

# List to store image file paths
image_files_quiver = []

sampling_factor = 25

for date in dates:
    wind_dir_gif = th_data.sel(day=date)['wind_from_direction']
    wind_speed_gif = vs_data.sel(day=date)['wind_speed']
    
    contour_vs_gif = vs_data.sel(day=date)
    
    # Sample the grid for plotting (e.g., reduce the number of vectors for clarity)
    wind_dir_sampled_gif = wind_dir_gif[::sampling_factor, ::sampling_factor]
    wind_speed_sampled_gif = wind_speed_gif[::sampling_factor, ::sampling_factor]
    lat_sampled_gif = wind_dir_sampled_gif.lat.values
    lon_sampled_gif = wind_dir_sampled_gif.lon.values
    
    # Convert wind speed and direction to u and v components
    u_gif = wind_speed_sampled_gif * np.cos(np.deg2rad(270 - wind_dir_sampled_gif))
    v_gif = wind_speed_sampled_gif * np.sin(np.deg2rad(270 - wind_dir_sampled_gif))
    
    # Create the quiver plot
    plt.figure(figsize=(10, 6))
    plt.quiver(lon_sampled_gif, lat_sampled_gif, u_gif, v_gif, color='orchid', scale=150)
    
    # Titles and labels
    # plt.colorbar(label="Wind Speed (m/s)")
    plt.title(f"Wind Vectors  on {str({date})}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save plot as an image file
    file_name = f"./dumps/quiver_plot_{date}.png"
    plt.savefig(file_name)
    image_files_quiver.append(file_name)  # Add file to the list of image files
    plt.close()

# Generate GIF using imageio
with imageio.get_writer("./animation/quiver_plots/quiver_animation_1.gif", mode='I', duration=2.5) as writer:
    for file_name in image_files_quiver:
        image = imageio.imread(file_name)
        writer.append_data(image)


# List to store image file paths
image_files_quiver = []

sampling_factor = 25

for date in dates:
    wind_dir_gif = th_data.sel(day=date)['wind_from_direction']
    wind_speed_gif = vs_data.sel(day=date)['wind_speed']
    
    contour_vs_gif = vs_data.sel(day=date)
    
    # Sample the grid for plotting (e.g., reduce the number of vectors for clarity)
    wind_dir_sampled_gif = wind_dir_gif[::sampling_factor, ::sampling_factor]
    wind_speed_sampled_gif = wind_speed_gif[::sampling_factor, ::sampling_factor]
    lat_sampled_gif = wind_dir_sampled_gif.lat.values
    lon_sampled_gif = wind_dir_sampled_gif.lon.values
    
    # Convert wind speed and direction to u and v components
    u_gif = wind_speed_sampled_gif * np.cos(np.deg2rad(270 - wind_dir_sampled_gif))
    v_gif = wind_speed_sampled_gif * np.sin(np.deg2rad(270 - wind_dir_sampled_gif))
    
    # Create the quiver plot
    plt.figure(figsize=(10, 6))
    plt.quiver(lon_sampled_gif, lat_sampled_gif, u_gif, v_gif, color='orchid', scale=500)
    
    # Titles and labels
    # plt.colorbar(label="Wind Speed (m/s)")
    plt.title(f"Wind Vectors  on {str({date})}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save plot as an image file
    file_name = f"./dumps/quiver_plot_{date}.png"
    plt.savefig(file_name)
    image_files_quiver.append(file_name)  # Add file to the list of image files
    plt.close()

# Generate GIF using imageio
with imageio.get_writer("./animation/quiver_plots/quiver_animation_2.gif", mode='I', duration=2.5) as writer:
    for file_name in image_files_quiver:
        image = imageio.imread(file_name)
        writer.append_data(image)
