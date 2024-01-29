# Quantlab: A solution for local stock database
- akshare: fetch online data
- MongoDB: store stock data locally

## Supported OS: Windows


## Setup python environment
```bash
conda create --name=quantlab python=3.8
conda activate quantdb
# pip install -r requirements.txt
pip install .
```

## Setup Mongodb in Docker
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop/). Make sure `docker` command is available in the command line.
```bash
docker --help
```
- Build a docker image containing `miniconda` and `mongodb`
```bash
cd akshare_db/docker
docker images -q my_image | docker build -t my_image .
```
- Start a docker image:
```bash
docker run -p 27017:27017 --name my_image my_image
```

- Close and save docker image:
```bash
docker ps # check all running images
docker commit my_image my_saved_image
docker stop my_image
```

- Refer to `akshare_db/docker/docker_commands.sh` for more frequently used docker commands


## Install MongoDBCompass
Connect to `localhost:27017` in MongoDBCompass

## Download Data after setups
- Download stock data
```bash
quantdb --help
quantdb --basic
quantdb --history --freq=daily --fq=hfq --start=20100101
```
- Don't forget to save the docker image with data:
```bash
docker commit my_image my_saved_image
```

