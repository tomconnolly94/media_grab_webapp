# Use the node image but install python3 on top of it
FROM node:slim

# Set the working directory to /src
WORKDIR /src

# Copy the current directory contents into the container at /app 
ADD . /src

# add python bins
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Install the dependencies
RUN pip3 install -r requirements.txt
RUN npm install --prefix ./client

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]

