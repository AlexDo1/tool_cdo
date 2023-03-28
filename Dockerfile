# Pull any base image that includes python3
FROM python:3.10

# install the toolbox runner tools
RUN pip install json2args

# install cdo binary, version 2.1.1
RUN echo "deb http://deb.debian.org/debian/ bookworm main" > /etc/apt/sources.list.d/bookworm.list \
    && apt-get update \
    && apt-get install -y cdo=2.1.1-1

# install cdo Python wrapper and dependencies
RUN pip install cdo xarray netCDF4

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["python", "run.py"]
