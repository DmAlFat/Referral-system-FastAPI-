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

---Стартовая страница---
--Получение приветственного сообщения--
[GET] http://127.0.0.1:8000/

---Блок авторизации (FastAPIUsers, JWT, CookieTransport)---
--Авторизация (При авторизации в качестве username используется исключительно email)--
[POST] http://127.0.0.1:8000//auth/jwt/login
--Выход из системы--
[POST] http://127.0.0.1:8000/auth/jwt/logout
--Регистрация (При введении действительного реферального кода Вы автоматически будете зарегистрированы в качестве реферала)--
[POST] http://127.0.0.1:8000/auth/register

---Функционал для авторизованных пользователей---
--Создание своего случайного реферального кода--
[GET] http://127.0.0.1:8000/functionality_for_authorized_users/create_referral_code
--Удаление своего реферального кода--
[GET] http://127.0.0.1:8000/functionality_for_authorized_users/delete_referral_code

---Функционал для всех пользователей---
--Получить реферальный код по email реферера--
[GET] http://127.0.0.1:8000/functionality_for_all_users/get_referral_code
--Получить информацию о рефералах по id реферера--
[POST] http://127.0.0.1:8000/functionality_for_all_users/receive_info_on_referrals


-----UI документация (Swagger/ReDoc)-----

--Swagger--
http://127.0.0.1:8000/docs
--ReDoc--
http://127.0.0.1:8000/redoc