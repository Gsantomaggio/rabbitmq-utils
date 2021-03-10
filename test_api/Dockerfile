## base image where to start
FROM python:3.6.13

## install the dependecies
RUN pip install -U Flask

# Copy your application to the image
COPY app.py  /myapp/app.py
WORKDIR /myapp

# how to the application starts
# when you execute the container
# the following commands are executesd
ENTRYPOINT ["python3","app.py"]