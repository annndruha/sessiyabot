# Marakulin Andrey @annndruha
# 2019

# Base image
FROM python:3.9.1-alpine3.13

# Add the main dirictory
ADD ./ update_users/

# Set that dirictory
WORKDIR update_users

# Update Base image
RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev && \
	pip install --no-cache-dir -r requirements.txt && \
	apk del build-deps

# Specify the port number the container should expose 
EXPOSE 1440

# Run the file
CMD ["python", "-u", "./update_users.py"]

# Example docker command:
# docker run -d --name update_users -v /root/update_users/config.py:/update_users/config.py imagename

# See logs:
# docker logs update_users --follow
