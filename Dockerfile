# our base image
FROM python:3

ADD ./Sessiya-bot/
#Sessiya-bot.py/

WORKDIR Sessiya-bot

# Addictional libraries
RUN pip3 install vk_api
RUN pip3 install wikipedia
RUN pip3 install pytz

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "./Sessiya-bot.py"]
