import os
from datetime import datetime as dt
import subprocess
from pprint import pprint

from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

# check if a toolname was set in env, default tool: sellonlatbox
toolname = os.environ.get('TOOL_RUN', 'sellonlatbox').lower()

# switch the tool
if toolname == 'sellonlatbox':
    print(kwargs)
    # run the command
    subprocess.Popen(f"cdo sellonlatbox,{kwargs['min_lon']},{kwargs['max_lon']},{kwargs['min_lat']},{kwargs['max_lat']} {kwargs['infile']} /out/outfile.nc")

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
