#! /bin/bash

#set variables
frontend_image='streamlit'
backend_image='fastapi'
frontend_container='Streamlit'
backend_container='FastApi'

# docker image rm -f $frontend_image
# docker image rm -f $backend_image

#remove container to prevent conflict
docker container -f $frontend_container
docker container -f $backend_container

#build images
cd streamlit
docker build -t $frontend_image .

cd ../fastapi
docker build -t $backend_image .

#create network with subnet 172.18.0.0/24
docker network create --subnet 172.18.0.0/24 CatvDogAppNet  

#run docker-compose file
docker-compose up


