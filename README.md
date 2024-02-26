# GeoData Processing Code

This repository contains Python code for processing geospatial data, particularly focused on extracting points from polygons and reindexing them based on their spatial properties.

## Overview

The provided code is designed to achieve the following:

1. Extract points from the exterior of polygons.
2. Ensure sequential numbering of points starting from the point with the maximum Y coordinate within each polygon.
3. Reindex the points accordingly.
4. Save the resulting points as a shapefile.


### Requirements

- Python 3.9
- Required Python packages: geopandas, pandas, shapely

### Instructions

1. Ensure all required packages are installed.
2. Replace the `POLYGON_SHAPEFILE` variable with the path to your input polygon shapefile.
3. Replace the `POLYGON_ID_FIELD` variable with your polygon unique id field name .
4. Run the script. It will generate a new shapefile containing the extracted points in your input polygon path.

## Functions

### `get_polygon_points(polygon_gdf)`

Extracts points from the exterior of each polygon in a GeoDataFrame.

- `polygon_gdf`: Input GeoDataFrame containing polygons.

### `get_shifted_points_gdf(points_gdf, shift_value)`

Shifts the IDs of points in a GeoDataFrame by a specified shift value.

- `points_gdf`: Input GeoDataFrame containing points.
- `shift_value`: The shift value to apply to the IDs.

### `get_shift_value(points_gpf, index_ID = INDEX_ID_FIELD)`

Calculates the shift value based on the maximum Y-coordinate point ID.

- `points_gpf`: A GeoDataFrame containing points.
- `index_ID`: The field name for the point ID.

## Files

- `your_code_file.py`: Python script containing the main code.
- `Points_(your polygon name).shp`: Output shapefile containing the extracted points.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

