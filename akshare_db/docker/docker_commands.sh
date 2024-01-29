# build an image from Dockerfile
docker images -q my_mongo_anaconda_image | docker build -t my_mongo_anaconda_image .

# download an image from cloud
docker images -q mongo || docker pull mongodb:latest

# list docker images
docker images

# run mongodb container in the detached mode/background process
docker run --name mongodb -d mongo

# run mongodb container and expose port
# -p, expose port to mongodb://localhost:27017
# -e MONGO_INITDB_ROOT_PASSWORD, init username and password
# -e MONGODB_CONNSTRING, connect to existing database
# -v, use volumes to make sure the data persists after the container stops
docker run --name mongodb \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=root \
    -e MONGODB_CONNSTRING=mongodb+srv://username:password@clusterURL MYAPP:1.0 \
    -v data-vol:/data/db \
    -d mongo:latest

# run interactive mongodb shell
# docker exec -it mongodb mongosh

# run interactive bash shell
docker exec -it mongodb bash

# list running images
docker ps

# save progress
docker commit mongodb my_saved_image

# close a running image: container_id or name
docker stop mongodb

# remove local image
docker rm mongodb