-----Установка-----
-Клонировать проект в пустую папку:
git clone https://github.com/DmAlFat/Referral-system-FastAPI-.git
-Установить необходимые модули:
pip install -r requirements.txt
-Задать параметры для подключения к Вашей базе данных PostgreSQL:
файл .env в корне проекта 


-----Запуск-----
-Запустить сервер:
uvicorn main:app --reload


-----Реализованные API-----

---Блок авторизации (FastAPIUsers, JWT, CookieTransport)---
--Авторизация (При авторизации в качестве username используется исключительно email)--
[POST] http://localhost:localport/auth/jwt/login
--Выход из системы--
[POST] http://localhost:localport/auth/jwt/logout
--Регистрация (При введении действительного реферального кода Вы автоматически будете зарегистрированы в качестве реферала)--
[POST] http://localhost:localport/auth/register

---Функционал для авторизованных пользователей---
--Создание своего случайного реферального кода--
[GET] http://localhost:localport/functionality for authorized users/create_referral_code
--Удаление своего реферального кода--
[GET] http://localhost:localport/functionality for authorized users/delete_referral_code

---Функционал для всех пользователей---
--Получить реферальный код по email реферера--
[GET] http://localhost:localport/functionality for all users/get_referral_code
--Получить информацию о рефералах по id реферера--
[POST] http://localhost:localport/functionality for all users/receive_info_on_referrals

---Стартовая страница---
--Получение приветственного сообщения--
[GET] http://localhost:localport/


-----UI документация (Swagger/ReDoc)-----

--Swagger--
http://localhost:localport/docs
--ReDoc--
http://localhost:localport/redoc