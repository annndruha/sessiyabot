#Base image
FROM python:3-alpine

#Add the main dirictory
ADD ./ Sessiya-bot/

#Set that dirictory
WORKDIR Sessiya-bot

# Addictional libraries for bot
RUN pip install vk_api pytz wikipedia

#Specify the port number the container should expose 
EXPOSE 5000

#Run the file
CMD ["python", "-u", "./Sessiya_bot.py"]

#docker run -d --name bot -v C:\Users\Andrey\source\repos\Annndruha\Sessiya_bot\users.txt:/Sessiya-bot/users.txt XXXXNAMEXXXX
