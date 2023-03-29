from datetime import datetime

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


    cdo.debug = True


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
        timeseries = cdo.fldmean(input = '-selregion,' + '/tmp/regions.txt' + ' -seldate,' + startdate + ',' + enddate + ' -mergetime ' + ' '.join(selected_files), returnArray = 'time, rainfall_amount')
    print(timeseries)
    #timeseries = temporal_mean.flatten()

    import matplotlib.pyplot as plt
    plt.plot(timeseries)
    plt.savefig("/out/timeseries.pdf")

    import numpy as np
    np.savetxt('/out/timeseries.csv', timeseries, delimiter=',')