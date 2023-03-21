from cdo import *


# initialize cdo
cdo = Cdo()

def sellonlatbox(min_lon: float, max_lon: float, min_lat: float, max_lat: float, infile: str):
    cdo.sellonlatbox(min_lon, max_lon, min_lat, max_lat, input = infile, output = '/out/outfile.nc')