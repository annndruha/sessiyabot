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

# Addictional libraries for bot
RUN pip install vk_api wikipedia

# Specify the port number the container should expose 
EXPOSE 5000

# Run the file
CMD ["python", "-u", "./sessiyabot.py"]

# Example docker command:
#docker run -d --name bot -v C:\Users\Andrey\source\repos\Annndruha\sessiyabot\data\config.py:/sessiyabot/data/config.py XXXXNAMEXXXX