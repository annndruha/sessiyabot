# Sessiya-bot
![Logo](https://sun9-28.userapi.com/c856020/v856020225/d2ad8/h3nhdDVN5qk.jpg)
## VK Chat-bot for students
Chatbot for students, which helps them prepare for the session, based on vk-community chat. See more in my community: https://vk.com/sessiyabot

Features:
+ Maintain conversation
+ Look for unknown on wikipedia
+ Solve math expressions
+ Send everyday reassuring message
+ Set exam date and time to send a reassuring message
+ Set up it by text and vk-keybord
+ Write data in PostgreSQL Database
+ Print logs

## Requirements
**First** of all, need to create **access token** in you vk-community and insert it in data/config.py

**Second**, you need to create **PostgreSQL** schema:
+ Name of schema - "sessiyabot" and a table name - "users"
+ Columns of "users" table: id, examdate, notifytime, subcribe, tz, firstname, lastname
+ Flags: "NotNone" flag for id, subcribe, tz
+ Default "false" for subcribe, default "0" for tz

And paste PostgreSQL settings like 'host, user, etc.' in data/config.py

**Language and time constants:**

Default code configurated for Moscow and Russian language. All language constants may change in data/ru_dictionary.py as well as exam date, but to change reference Moscow timezone(UTC+3) (using to write in database) you need open func/datetime_functions.py. Also you need to change wikipedia language: core/engine find_in_internet in request string. Logs timestamp always in UTC timezone.

### Supported Python Version
Python 3.7 are fully  tested.

### Third Party Libraries and Dependencies
The following libraries must be installed when using sessiyabot:
```bash
psycopg2==2.8.3
vk-api==11.5.0
```

### Docker
If you use  docker, you can run bot with this example docker command:
```bash
docker run -d --name sessiyabot imaginename
```
Or this, if you want to keep config data in secret:
```bash
docker run -d --name sessiyabot -v /root/sessiyabot/configvolume.py:/sessiyabot/data/config.py imaginename
```
See logs:
```bash
docker logs sessiyabot -follow
```
## Project imports schema:
![Schema](https://sun9-22.userapi.com/c857736/v857736714/59499/kxmdJLOJl_4.jpg)
