# Use the node image but install python3 on top of it
FROM nikolaik/python-nodejs:python3.6-nodejs14

# Set the working directory to /app
WORKDIR /src

# Copy the current directory contents into the container at /app 
ADD . /src

# Install the dependencies
RUN pip install -r requirements.txt
RUN npm install --prefix ./client

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]

