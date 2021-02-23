name = "GOES"
from .downloads.download_data import *
from .processing.processing_data import *
__all__ = ['show_products','download_file', 'download',
           'GOES', 'open_dataset', 'open_mfdataset',
           'get_lonlat','get_lonlatcorner','corner_size_to_center_size',
           'midpoint_in_x','midpoint_in_y','calculate_corners',
           'find_pixel_of_coordinate',
           'cosine_of_solar_zenith_angle',
           'find_pixels_of_region','create_gridmap','accumulate_in_gridmap',
           'locate_files']
__version__ = '3.2'
