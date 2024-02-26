import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry import Point


INDEX_ID_FIELD = 'index_ID'  # Point index_ID field name 
NEW_ID_FIELD = 'Point_ID'  # field name for the NEW Point_ID (shifted_id)

def get_shift_value(points_gpf, index_ID = INDEX_ID_FIELD ):
    """
    Calculates the shift value based on the maximum y-coordinate point ID.

    Parameters:
        points_gpf (GeoDataFrame): A GeoDataFrame containing points.
        index_ID (str): The field name for the point ID.

    Returns:
        int: The shift value.
    """
    max_y = points_gpf.geometry.y.max()
    max_y_point_id = points_gpf.loc[points_gpf.geometry.y == max_y, index_ID].values[0]
    shift_value = abs(max_y_point_id - 1)
    return shift_value

def get_shifted_id(old_id, shift_value, num_of_all_points):
    """
    Shifts the given ID by a certain value.

    Parameters:
        old_id (int): The original ID.
        shift_value (int): The amount by which to shift the ID.
        num_of_all_points (int): The total number of all points.

    Returns:
        int: The shifted ID.
    """
    new_id = old_id - shift_value
    if new_id <= 0:
        return new_id + num_of_all_points 
    else:
        return new_id

def get_shifted_points_gdf(points_gdf, shift_value):
    """
    Shifts the IDs of points in a GeoDataFrame by a specified shift value.

    Parameters:
        points_gdf (GeoDataFrame): A GeoDataFrame containing points.
        shift_value (int): The shift value to apply to the IDs.

    Returns:
        GeoDataFrame: The GeoDataFrame with shifted IDs.
    """
    points_num = len(points_gdf)
    points_gdf[NEW_ID_FIELD] = [get_shifted_id(row[INDEX_ID_FIELD], shift_value, points_num) for _, row in points_gdf.iterrows()]
    # Convert the new column to long integer
    # unnecessary but just in case you use the points id for map series in ArcGIS Pro
    points_gdf[NEW_ID_FIELD] = points_gdf[NEW_ID_FIELD].astype('int64')  
    points_gdf.drop(columns=[INDEX_ID_FIELD], inplace=True)  # Delete the INDEX_ID_FIELD column
    return points_gdf


def get_polygon_points(polygon_gdf):
    """
    Extracts points from the exterior of each polygon in a GeoDataFrame
    and ensures the sequential numbering of the points starts at the point with the maximum Y coordinate.

    Parameters:
        polygon_gdf (GeoDataFrame): A GeoDataFrame containing polygons.

    Returns:
        GeoDataFrame: A GeoDataFrame containing points extracted from the polygons.
    """
    shifted_points_list = []  #create an empty list for all Polygon's points
    #loop  through all features in the input geodataframe
    for _ , row in polygon_gdf.iterrows():
        #check if  geometry is Polygon or MultiPolygon
        if not isinstance(row['geometry'], Polygon):
            print(f"Geometries with ID {row[POLYGON_ID_FIELD]} are not a Polygon.")
            continue

        points_list = []  #create an empty list for current Polygon points
        #loop through all exterior coords for the current Polygon
        for index , coord in enumerate(list(row['geometry'].exterior.coords)[:-1], 1):
            point_geometry = Point(coord) #shapely point geometry
            # Create point data including index ID, polygon ID, and geometry
            point_data = {
                          INDEX_ID_FIELD : index,
                          POLYGON_ID_FIELD: row[POLYGON_ID_FIELD],
                          'geometry': point_geometry
                          }
            #add current point data to the total list of points for current Polygon
            points_list.append(point_data) 

        # Make points geodataframe for current Polygon 
        points_gdf = gpd.GeoDataFrame(points_list)  
        #get shift  value for current Polygon
        shift_value = get_shift_value(points_gdf) 
        # Get points GeoDataFrame for the current Polygon after applying the shift value to the INDEX_ID_FIELD
        shifted_points_gdf = get_shifted_points_gdf(points_gdf, shift_value) 
        #add to the total list of all Polygon's points
        shifted_points_list.append(shifted_points_gdf)  

    if shifted_points_list:
        # concatenad all point geodataframes in the shifted_points_list
        merged_shifted_points_gdf = gpd.GeoDataFrame(pd.concat(shifted_points_list, ignore_index=True))
        # Set the coordinate system to be same as polygon coordinate system
        merged_shifted_points_gdf.crs = polygon_gdf.crs 

        return merged_shifted_points_gdf
    else:
        print("No valid polygons found!")
        return None


if '__main__' == __name__:
   
    POLYGON_SHAPEFILE = r"path\to\Polygon.shp"
    POLYGON_ID_FIELD = "Polygon_UID"
    
    output_folder = os.path.dirname(POLYGON_SHAPEFILE)
    output_point_name = 'Points_' + os.path.basename(POLYGON_SHAPEFILE)
    output_point_path = os.path.join(output_folder, output_point_name)

    if POLYGON_SHAPEFILE.lower().endswith('shp'):
        polygon_gdf = gpd.read_file(POLYGON_SHAPEFILE)
        all_points_gdf = get_polygon_points(polygon_gdf)
        if not all_points_gdf.empty:
            all_points_gdf.to_file(output_point_path, driver='ESRI Shapefile')
            print(f"Successfully Extracted polygon corners Point to the shapefile: {output_point_path}")
    else:
        print(f"{POLYGON_SHAPEFILE} is not a ESRI Shapefile.")
