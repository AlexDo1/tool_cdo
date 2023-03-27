import os
from datetime import datetime as dt

from cdo import *
from cdolib import *
from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

# check if a toolname was set in env, default tool: sellonlatbox
toolname = os.environ.get('TOOL_RUN', 'sellonlatbox').lower()

# switch the tool
if toolname == 'sellonlatbox':
    # get the parameters
    try:
        infile = kwargs['infile']
        min_lon, max_lon, min_lat, max_lat = kwargs['min_lon'], kwargs['max_lon'], kwargs['min_lat'], kwargs['max_lat']
    except Exception as e:
        print(str(e))
        sys.exit(1)

    # run the command
    sellonlatbox(min_lon, max_lon, min_lat, max_lat, infile)

elif toolname == 'seldate':
    # get the parameters
    try:
        infile = kwargs['infile']
        startdate, enddate = kwargs['startdate'], kwargs['enddate']
    except Exception as e:
        print(str(e))
        sys.exit(1)

    # run the command
    seldate(startdate, enddate, infile)

elif toolname == 'seldate_sellonlatbox':
    # get the parameters
    try:
        infile = kwargs['infile']
        startdate, enddate = kwargs['startdate'], kwargs['enddate']
        min_lon, max_lon, min_lat, max_lat = kwargs['min_lon'], kwargs['max_lon'], kwargs['min_lat'], kwargs['max_lat']
    except Exception as e:
        print(str(e))
        sys.exit(1)

    # run the command
    seldate_sellonlatbox(startdate, enddate, min_lon, max_lon, min_lat, max_lat, infile)
    
# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
