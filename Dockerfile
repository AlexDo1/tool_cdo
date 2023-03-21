# Pull any base image that includes python3
FROM python:3.10

# install the toolbox runner tools
RUN pip install json2args

# install cdo binary
RUN apt-get update && apt-get install -y cdo

# install cdo Python wrapper
RUN pip install cdo

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["python", "run.py"]
