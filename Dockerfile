# sessiyabot/Dockerfile
# -docker container settings
# Config file needs to add MANUALLY
# Ìàðàêóëèí Àíäðåé @annndruha
# 2019

# Base image
FROM python:3-alpine

# Add the main dirictory
ADD ./ sessiyabot/

# Set that dirictory
WORKDIR sessiyabot

# Addictional libraries for bot
RUN pip install vk_api psycopg2

# Specify the port number the container should expose 
EXPOSE 5000

# Run the file
CMD ["python", "-u", "./sessiyabot.py"]

# Example docker command:
#docker run -d --name bot -v /root/config.py:/sessiyabot/data/config.py XXXXNAMEXXXX
