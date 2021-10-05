# Use the node image but install python3 on top of it
FROM nikolaik/python-nodejs:latest

# Set the working directory to /app
WORKDIR /src

# Copy the current directory contents into the container at /app 
ADD . /src

# Install the dependencies
RUN pip install -r requirements.txt

WORKDIR "client"
RUN npm install
WORKDIR "../"

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]

