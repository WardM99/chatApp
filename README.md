# chatApp
A simple opensource chatApp
## Backend
[![codecov](https://codecov.io/gh/WardM99/chatApp/graph/badge.svg?token=3041EE1S3Y)](https://codecov.io/gh/WardM99/chatApp)
### Run backend
To run the backend you can use docker.
```console
# navigate to backend
cd backend
# build docker image
docker build -t chatappbackend .
# run docker image
docker run -d --name mycontainer -p 80:80 chatappbackend
```
If you want to see the docker console in your console
```console
docker run --name mycontainer -p 80:80 chatappbackend
```
