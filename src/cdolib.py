from cdo import *


# initialize cdo
cdo = Cdo()

def sellonlatbox(min_lon: float, max_lon: float, min_lat: float, max_lat: float, infile: str):
    """
    Selects all timesteps with a date in a user given range.
    
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
    