# sessiyabot/Dockerfile
# -docker container settings
# Config file needs to add MANUALLY
# Маракулин Андрей @annndruha
# 2019

# Base image
FROM python:3-alpine

# Add the main dirictory
ADD ./ sessiyabot/

# Set that dirictory
WORKDIR sessiyabot

# Update Base image
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
    
# Addictional libraries for bot
RUN pip install vk_api psycopg2-binary

# Specify the port number the container should expose 
EXPOSE 5000

# Run the file
CMD ["python", "-u", "./sessiyabot.py"]

# Example docker command:
#docker run -d --name bot -v /root/config.py:/sessiyabot/data/config.py XXXXNAMEXXXX
