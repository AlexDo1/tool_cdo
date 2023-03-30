from datetime import datetime

import numpy as np
import pandas as pd

from cdo import *


# initialize cdo
cdo = Cdo()

def dwd_radar_to_timeseries(nc_folder, shape_geojson, startdate, enddate, mode):
    """
    

    Parameters
    ----------
    nc_folder: str
        Path to folder containing daily split netCDF files with
        the year, month and day as the start of the filename in 
        the following format: %Y%m%d (e.g. 20010101_radolan_rw.nc).
    shape_geojson: str
        Path to geojson file containing the shape of the region to 
        be selected.
    startdate: str
        Start date (format YYYY-MM-DDThh:mm:ss).
    enddate: str
        End date (format YYYY-MM-DDThh:mm:ss).
    mode: str
        Data aggregation mode ['mean']

    """
    ### select files in given temporal range from nc_folder
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

    ### process geojson shape for input into selregion
    # read geojson shape
    with open(shape_geojson, 'r') as j:
        contents = json.loads(j.read())

    # create ASCII file to store polygon coordinates
    f = open('/tmp/regions.txt', 'w')

    # write coordinates to ASCII file
    # TODO: make this more flexible (keys)?
    for lon, lat in contents.get('features')[0]['geometry']['coordinates'][0]:
        f.writelines([str(lon), ' ', str(lat), '\n'])

    
    # operators: mergetime - selregion - seldate - aggregate: timmean
    if mode == 'mean':
        ds = cdo.fldmean(input = '-selregion,' + '/tmp/regions.txt' + ' -seldate,' + startdate + ',' + enddate + ' -mergetime ' + ' '.join(selected_files), 
                                 returnXArray=['time', 'rainfall_amount'])

    # Extract the 'time' and 'rainfall_amount' variables from the xarray dataset
    time = ds.time.values
    rainfall_amount = ds.rainfall_amount.values

    # Convert time array to minute precision by rounding down to nearest minute, add 30 seconds to make sure that rounding down is always correct
    time = np.datetime64(time.astype('datetime64[m]') + np.timedelta64(30, 's'), unit='m')
    
    # Create a pandas dataframe with the two variables    
    df = pd.DataFrame({'time': time, 'rainfall_amount': rainfall_amount.reshape(-1)})

    # Write the dataframe to a CSV file
    df.to_csv('/out/timeseries.csv', index=False)

    # plot rainfall_amount against time and save as PDF
    fig = df.plot.line(x='time', y='rainfall_amount').get_figure()
    fig.savefig("/out/timeseries.pdf")
