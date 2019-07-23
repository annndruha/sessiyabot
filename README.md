# Sessiya-bot

Чат-бот ВК для студентов. Позволяет отправлять напоминания и отвечать на простые вопросы.

Sessiya_bot - основной файл с двумя потоками, один отвечает за чат, другой за напоминания
Chat_module - движок анализа текста пользовательского запроса
Notification_module - напоминания
Engine - файл с некоторыми полезными функциями, такими как поиск в википедии, склонением по падежам и др.
Dictionary - словарь ключевых слов для бота, по которым ведётся поиск подходящего ответа
Datebase functions - функции работы с 'базой данных' пользователей
User list - база id пользователей с настройками даты экзамена, времени напоминаний, подпиской на рассылку
Config - файл с глобальными параметрами

+файл инициализации питон
+dockerfile с настройкой контейнера docker