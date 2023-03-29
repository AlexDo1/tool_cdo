import os
import json
from datetime import datetime

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
    Select cells inside regions.
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
    f = open('/tmp/regions.txt', 'w')

    # write coordinates to ASCII file
    # TODO: make this more flexible (keys)?
    for lon, lat in contents.get('features')[0]['geometry']['coordinates'][0]:
        f.writelines([str(lon), ' ', str(lat), '\n'])

    # execute cdo command
    cdo.selregion('/tmp/regions.txt', input = infile, output = '/out/outfile.nc')


def mergetime(nc_folder, startdate, enddate):
    """
    Merge datasets sorted by date and time.
    Provide a folder with daily split netCDF files together with
    a startdate and an enddate, files are selected by the date 
    contained in the filename and are then merged.  
    After that, the cdo operator seldate is used to clip the 
    netCDF to the temporal range given in startdate and enddate.
    
    Parameters
    ----------
    nc_folder: str
        Path to folder containing daily split netCDF files with
        the year, month and day as the start of the filename in 
        the following format: %Y%m%d (e.g. 20010101_radolan_rw.nc).
    startdate: str
        Start date (format YYYY-MM-DDThh:mm:ss).
    enddate: str
        End date (format YYYY-MM-DDThh:mm:ss).

    """
    # convert startdate and enddate strings to datetime objects
    startdate_dt = datetime.strptime(startdate, '%Y-%m-%dT%H:%M:%S').date()
    enddate_dt = datetime.strptime(enddate, '%Y-%m-%dT%H:%M:%S').date()

    # get list of files in folder
    files = os.listdir(nc_folder)

    # get base directory name
    dirname = os.path.basename(os.path.normpath(nc_folder))

    # loop over files and select those with date within startdate and enddate
    selected_files = []
    for file in files:
        if file.endswith('.nc'):
            filedate_str = file[:8]
            filedate = datetime.strptime(filedate_str, '%Y%m%d').date()
            if startdate_dt <= filedate <= enddate_dt:
                selected_files.append(f"/in/{dirname}/{file}")

    # sort selected files
    selected_files = sorted(selected_files)

    # operator chain: merge selected files, select specified temporal range
    cdo.seldate(startdate, enddate, input = "-mergetime " + ' '.join(selected_files), output = '/out/outfile.nc')