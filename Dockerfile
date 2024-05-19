# Use the official Python image from the Docker Hub
FROM python:3.12

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE $port

# Define environment variable
# ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD gunicorn --workers=4 --bind 0.0.0.0:$port app:app
