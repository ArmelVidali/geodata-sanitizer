import geopandas as gpd
import overpy
from pyproj import Proj, transform
import json


def convert(geo_dataframe, file_name, output_path, output_format, target_crs=False):

    if target_crs:
        geo_dataframe = geo_dataframe.to_crs(target_crs)

    if output_format == "csv":
        geo_dataframe.to_csv(f"{output_path}/{file_name}.{output_format}")
    else:
        geo_dataframe.to_file(f"{output_path}/{file_name}.{output_format}")


def import_data(path):

    try:

        gdf = gpd.read_file(path)

        return gdf

    except Exception as err:
        return None, f"Error importing data: {err}"
