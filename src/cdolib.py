import json

from cdo import *


# initialize cdo
cdo = Cdo()

def sellonlatbox(min_lon: float, max_lon: float, min_lat: float, max_lat: float, infile: str):
    """
    Selects grid cells inside a lon/lat box.
    
    Parameters
    ----------
    min_lon: float
        Western longitude in degrees.
    max_lon: float
        Eastern longitude in degrees.
    min_lat: float
        Southern or northern latitude in degrees.
    max_lat: float
        Northern or southern latitude in degrees.
    infile: str
        Path to input file which is processed.
    
    """
    cdo.sellonlatbox(min_lon, max_lon, min_lat, max_lat, input = infile, output = '/out/outfile.nc')


def seldate(startdate: str, enddate: str, infile: str):
    """
    Selects all timesteps with a date in a user given range.
    
    Parameters
    ----------
    startdate: str
        Start date (format YYYY-MM-DDThh:mm:ss).
    enddate: str
        End date (format YYYY-MM-DDThh:mm:ss).
    infile: str
        Path to input file which is processed.
    
    """
    cdo.seldate(startdate, enddate, input = infile, output = "/out/outfile.nc")


def seldate_sellonlatbox(startdate: str, enddate: str, min_lon: float, max_lon: float, min_lat: float, max_lat: float, infile: str):
    """
    Selects all timesteps with a date in a user given range and
    selects grid cells inside a lon/lat box.
    
    Parameters
    ----------
    min_lon: float
        Western longitude in degrees.
    max_lon: float
        Eastern longitude in degrees.
    min_lat: float
        Southern or northern latitude in degrees.
    max_lat: float
        Northern or southern latitude in degrees.
    startdate: str
        Start date (format YYYY-MM-DDThh:mm:ss).
    enddate: str
        End date (format YYYY-MM-DDThh:mm:ss).
    infile: str
        Path to input file which is processed.
    
    """
    cdo.sellonlatbox(min_lon, max_lon, min_lat, max_lat, input = f"-seldate,{startdate},{enddate} {infile}", output = "/out/outfile.nc")


def selregion(shape_geojson, infile):
    """
    Select cells inside regions
    Selects all grid cells with the center point inside the regions. 
    The user has to give file in geojson format which contains the 
    coordinates of the region which is to be selected from the netCDF
    file.
    If you only have a shape file of your region, you can use a tool
    like ogr2ogr to convert it to a geojson file.
    
    Parameters
    ----------
    shape_geojson: str
        Path to geojson file containing the shape of the region to 
        be selected.
    infile: str
        Path to input file which is processed.

    """
    # read geojson shape
    with open(shape_geojson, 'r') as j:
        contents = json.loads(j.read())

    # create ASCII file to store polygon coordinates
    f = open('/out/regions.txt', 'w')

    # write coordinates to ASCII file
    # TODO: make this more flexible (keys)?
    for lon, lat in contents.get('features')[0]['geometry']['coordinates'][0]:
        f.writelines([str(lon), ' ', str(lat), '\n'])

    import os
    print(os.system('cdo --version'))
    # execute cdo command
    cdo.selregion('/out/regions.txt', input = infile, outfile = '/out/outfile.nc')