name = "GOES"
from .download.download_data import show_download_options
from .download.download_data import download_from_amazon
from .navigation.gets_navigation import get_lonlat
from .navigation.gets_navigation import midpoint_in_x
from .navigation.gets_navigation import midpoint_in_y
from .navigation.gets_navigation import get_lonlat_corners
from .navigation.gets_navigation import nearest_pixel
from .navigation.gets_navigation import slice_sat_image
from .navigation.gets_navigation import slice_area
from .navigation.gets_navigation import calc_cos_teta
from .navigation.gets_navigation import calc_orbital_factor
__version__ = '0.0.1'
