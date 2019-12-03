# Sessiya-bot

![Logo](https://camo.githubusercontent.com/29fe12ed3ec7c9493f63eab6ce2f76a8ee6ebff2/68747470733a2f2f73756e392d32382e757365726170692e636f6d2f633835363032302f763835363032303232352f64326164382f68336e686444564e35716b2e6a7067)

## VK Chat-bot for students

Chatbot for students, which helps them prepare for the session, based on vk-community chat. See more in my community: <https://vk.com/sessiyabot>

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

Example of data/config.py
access_token = 'your_vk_token'
db_host = '0.0.0.0'
db_port = '5432'
db_name = 'template1'
db_account = 'username'
db_password = 'userpassword'

**Second**, you need to create **PostgreSQL** schema:

+ Name of schema - "sessiyabot" and a table name - "users"
+ Columns of "users" table: id, examdate, notifytime, subcribe, tz, firstname, lastname
+ Flags: "NotNone" flag for id, subcribe, tz
+ Default "false" for subcribe, default "0" for tz

And paste PostgreSQL settings like 'host, user, etc.' in data/config.py

**Language and time constants:**
Default code configurated for Moscow and Russian language. All language constants may change in data/ru_dictionary.py as well as exam date, but to change reference Moscow timezone(UTC+3) (using to write in database and logs) you need change four functions (datetime_now_obj in datetime_func and 3 timestamps in chat, notify and vk module). Also you need to change wikipedia language: core/engine find_in_internet in request string.

### System

Supported Windows and Ubuntu
Python 3.7

### Third Party Libraries and Dependencies

The following libraries must be installed when using sessiyabot:

```bash
psycopg2==2.8.3
vk-api==11.5.0
```

### Docker

If you use  docker, you can run bot with this example docker command:

```bash
docker run -d --name sessiyabot imagename
```

Or this, if you want to keep config data in secret:

```bash
docker run -d --name sessiyabot -v /root/sessiyabot/configvolume.py:/sessiyabot/data/config.py imagename
```

See logs:

```bash
docker logs sessiyabot -follow
```

## Project imports schema

![Schema](https://camo.githubusercontent.com/abf77df95628ee77413d6bfc5658ed0b64e8ccaa/68747470733a2f2f73756e392d32322e757365726170692e636f6d2f633835373733362f763835373733363731342f35393439392f6b786d644a4c4f4a6c5f342e6a7067)
