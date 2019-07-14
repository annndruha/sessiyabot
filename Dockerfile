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

#Run the files
RUN ./Sessiya-bot.py
RUN ./Timer_bot.py
#CMD ["python", "./Sessiya-bot.py"]
#CMD ["python", "./Timer_bot.py"]
