# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot script when the container launches
CMD ["python", "./telegram_rss.py"]

# DOCKER COMMANDS:
# build the image like this:
# docker build -t name-of-your-docker-image .

# run the container like this:
# docker run --restart=always --name name-of-your-docker-container -v /Users/location-of-your-repo-folder/:/app name-of-your-docker-image

# inspect temp container
# docker run --rm -it name-of-your-docker-image ls /app
