from datetime import datetime

import numpy as np
import pandas as pd

from cdo import *


# initialize cdo
cdo = Cdo()


def aggregate_netcdf(nc_folder: str, variable: str, shape_geojson: str, startdate: str, enddate: str, mode: str) -> None:
    """
    The function aggregate_netcdf processes netCDF files containing a 
    specific variable within a given geographical region and temporal 
    range. It aggregates the data using a specified mode and saves the 
    output as a CSV file and a PDF plot.

    Parameters
    ----------
    nc_folder: str
        Path to folder containing daily split netCDF files with
        the year, month and day as the start of the filename in 
        the following format: %Y%m%d (e.g. 20010101_radolan_rw.nc).
    variable: str
        The variable contained in the netCDF files that is aggregated.
        Note, that the tstamp coordinate has to be named 'time'.
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
    # TODO: make this more flexible (keys)?
    with open('/tmp/regions.txt', 'w') as f:
        # write coordinates to ASCII file
        for lon, lat in contents.get('features')[0]['geometry']['coordinates'][0]:
            f.writelines([str(lon), ' ', str(lat), '\n'])

    # operators: mergetime - seldate - selregion - aggregate
    if mode == 'mean':
        ds = cdo.fldmean(input = '-selregion,' + '/tmp/regions.txt' + ' -seldate,' + startdate + ',' + enddate + ' -mergetime ' + ' '.join(selected_files),
                         returnXArray=['time', variable])

    # Extract the 'time' and variable from the xarray dataset
    time = ds.time.values
    variable_data = ds[variable].values

    # Convert time array to minute precision by rounding down to nearest minute, add 30 seconds to make sure that rounding down is always correct
    time = pd.to_datetime(time).round('min').values.astype('datetime64[s]')
    
    # Create a pandas dataframe with the two variables    
    df = pd.DataFrame({'time': time, variable: variable_data.reshape(-1)})

    # Write the dataframe to a CSV file
    df.to_csv('/out/timeseries.csv', index=False)

    # plot variable against time and save as PDF
    fig = df.plot.line(x='time', y=variable, ylabel=variable).get_figure()
    fig.savefig("/out/timeseries.pdf")
