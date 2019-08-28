# sessiyabot/Dockerfile
# -docker container settings
# Config file needs to add MANUALLY
# Marakulin Andrey @annndruha
# 2019

# Base image
FROM python:3-alpine

# Add the main dirictory
ADD ./ sessiyabot/

# Set that dirictory
WORKDIR sessiyabot

# Update Base image
RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk del build-deps

# Specify the port number the container should expose 
EXPOSE 42

# Run the file
CMD ["python", "-u", "./sessiyabot.py"]

# Example docker command:
# docker run -d --name bot -v /root/sessiyabot/configvolume.py:/sessiyabot/data/config.py XXXXNAMEXXXX

# See logs:
# docker logs bot --follow