#Base image
FROM python:3-alpine

#Add the main dirictory
ADD ./ Sessiya-bot/

#Set that dirictory
WORKDIR Sessiya-bot

# Addictional libraries for bot
RUN apk add --no-cache gcc musl-dev && --no-cache-dir && pip install && pip install vk_api && pip install wikipedia pytz

#Specify the port number the container should expose 
EXPOSE 5000

#Run the file
CMD ["python", "./Sessiya_bot.py"]

#docker run -d --name bot -v C:\Users\Andrey\source\repos\Annndruha\Sessiya-bot\users.txt:/Sessiya-bot/users.txt 2a9d81d1a5d6
