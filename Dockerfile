#Base image
FROM python:3

#Add the main dirictory
ADD ./ Sessiya-bot/

#Set that dirictory
WORKDIR Sessiya-bot

# Addictional libraries for bot
RUN pip3 install vk_api
RUN pip3 install wikipedia
RUN pip3 install pytz

#Specify the port number the container should expose 
EXPOSE 5000

#Run the file
CMD ["python", "./Sessiya_bot.py"]
