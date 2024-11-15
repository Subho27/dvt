# Project Documentation

This repository contains all the resources for the project, including documentation, figures, and the codebase. The project is divided into three main folders: `Document`, `Figures`, and `Codebase`.

## Folder Structure

- **Document**: Contains the documentation for our work.
- **Figures**: Contains all the figures used in the documentation, including high-quality images, Gephi files, animations, and extra files generated during the project.
- **Codebase**: Contains all the code written for the assignment.

---

## Document Folder

The `Document` folder contains a PDF file that details the work and findings of the project. To view the documentation, use any PDF reader software such as [Adobe Acrobat](https://get.adobe.com/reader/).

---

## Figures Folder

The `Figures` folder includes various images and GIF files. Use any image or GIF viewing application to view them.

To view the Gephi files:
1. Install [Gephi](https://gephi.org/) software.
2. Upload the Gephi files from this folder to Gephi.

---

## Codebase Folder

The `Codebase` folder is divided into the following subfolders:

### Task I - SciVis

Contains files and directories for generating visualizations, including contour plots, heatmaps, and quiver plots.

- **_DATASET**: Contains the data used for the visualizations.
- **animation**: Stores folders for the resultant animations, including `contour`, `heatmap`, and `quiver`.
- **dumps**: Stores intermediate images for development purposes.
- **Scivis Contour Plot.py**: Generates contour plot animations for various variables such as near-surface humidity, temperature, precipitation, and more. 
  - Simply run this file to generate the output. 
  - Output will be saved in `animation/contour_plots` (inside `marching_squares` and `contour_fill`).

- **Scivis Heatmap Plot.py**: Generates heatmap plot animations for various environmental variables.
  - Run this file to generate the output.
  - Output will be saved in `animation/heatmap_plots`.

- **Scivis Quiver Plot.py**: Generates quiver plot animations for wind speed and direction.
  - Run this file to generate the output.
  - Output will be saved in `animation/quiver_plots`.

### Task II - Graph Layout Algorithms

Contains files for graph layout visualizations.

- **_DATASET**: Contains the data used for graph layout.
- **Graph Layout Wikipedia.py**: A Python script to preprocess the data for use with Gephi.
- **output**: Stores the preprocessed files for use in Gephi.
- Final graph layouts can be visualized using Gephi.

### Task III - InfoVis

Contains files for generating visualizations such as Parallel Coordinates Plot (PCP) and Treemaps.

- **_DATASET**: Contains the raw data for the visualizations.
- **_PCP_DATA**: Contains preprocessed data used for PCP visualizations.
- **_TREEMAP_DATA**: Contains preprocessed data used for Treemap visualizations.
- **py**: Contains Python scripts for preprocessing the raw data.
- HTML files are used to display the final visualizations as interactive web pages.

---

## Steps to Reproduce

### Contour Plot
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task I - SciVis`.
3. Run the file `Scivis Contour Plot.py`.
4. The output animations will be generated in `animation/contour_plots` (in `marching_squares` and `contour_fill`).
5. If there is an exception, try running the file again as local machine limitations might cause issues with large data.

### Heatmap Plot
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task I - SciVis`.
3. Run the file `Scivis Heatmap Plot.py`.
4. The output animations will be generated in `animation/heatmap_plots`.
5. If there is an exception, try running the file again due to potential issues with large data.

### Quiver Plot
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task I - SciVis`.
3. Run the file `Scivis Quiver Plot.py`.
4. The output animations will be generated in `animation/quiver_plots`.
5. If there is an exception, try running the file again due to potential issues with large data.

### Graph Layout
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task II - Graph Layout Algorithms`.
3. Run the file `Graph Layout Wikipedia.py`.
4. The output will be saved in the `output` folder.
5. After preprocessing, upload the output files to Gephi and use graph layout algorithms to generate the final output.

### PCP Plots
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task III - InfoVis`.
3. Run the files `py/Parallel Coordinates Plot I.py` and `py/Parallel Coordinates Plot II.py`.
4. The preprocessed files will be saved in `_PCP_DATA`.
5. Open the following HTML files to view the PCP visualizations:
   - `pcp_crime_rate.html`
   - `pcp_crime_state_rate_1.html`
   - `pcp_crime_state_rate_2.html`
   - `pcp_crime_state_rate_3.html`

### Treemap Plots
1. Ensure no files or folders are replaced or removed.
2. Navigate to `Task III - InfoVis`.
3. Run the files `py/TreeMap Visualization I.py`, `py/TreeMap Visualization II.py`, and `py/TreeMap Visualization III.py`.
4. The preprocessed files will be saved in `_TREEMAP_DATA`.
5. Open the following HTML files to view the Treemap visualizations:
   - `treemap_crime_rate.html`
   - `treemap_crime_rate_anti_corruption.html`
   - `treemap_crime_rate_place.html`
6. Click on each section to see detailed information inside that section.

---

## Extra
This project provides a comprehensive suite of visualizations for climate, graph layout algorithms, and crime-related data using SciVis, InfoVis, and graph layout techniques. Ensure that the necessary software (Python, Gephi, and a web browser) is installed to view and interact with the visualizations. For any issues or questions, please feel free to reach out.

