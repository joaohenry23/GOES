name = "GOES"
help1 = 'help(GOES.downloads.download_data)'
help2 = 'help(GOES.navigation.gets_navigation)'
from .downloads.download_data import show_products
from .downloads.download_data import download_file
from .downloads.download_data import download
from .navigation.gets_navigation import get_lonlat
from .navigation.gets_navigation import midpoint_in_x
from .navigation.gets_navigation import midpoint_in_y
from .navigation.gets_navigation import get_lonlat_corners
from .navigation.gets_navigation import nearest_pixel
from .navigation.gets_navigation import slice_sat_image
from .navigation.gets_navigation import slice_area
from .navigation.gets_navigation import calc_cos_teta
from .navigation.gets_navigation import calc_orbital_factor
__version__ = '0.0.2'
