# Telegram Collector
___
## About the project:
This project is a tool designed to collect and manage messages from Telegram chats using a bot. 
The collected messages are saved in JSON format within a **Postgres** database. 
Administrators can get access to the **REST** service with secure **JWT** authentication to view messages, monitor active chats, connect to chats via **Websocket**, and even send messages from the bot. 

The application is built using **Python** and leverages the power of asynchronous frameworks:
- **FastAPI**
- **Tortoise ORM**
- **aiogram**
- **pydantic**
- **uvicorn**
- **pytest**

Additionally, the app is deployable and customizable through **Docker**.

### Features:
- _Message Collection_: The application collects messages from Telegram chats using a bot and saves them in JSON format within a Postgres database.
- _Telegram bot_: To collect messages, add bot to the chat and give it access to chat messages.
- _REST API_: Administrators can get access to saved messages through the REST service.
- _JWT authentication_: JSON Web Tokens are used to authenticate administrators.
- _Asynchronous Python_: The application is built using asynchronous Python for scalability and efficiency.
- _Docker Support_: The application is easily deployable in Docker using prepared config files.
- _Websocket_: Websocket connection allows an administrator receive and send chat messages through the bot in real-time.
- _FSM_: A basic Finite State Machine implementation allows users to rate this bot. REST API allows administrators to view all active states.

___
## Installation
**1.** Clone this repository.

**2.** Create Telegram bot via @BotFather. 
Copy and save the Telegram bot's access token.

**3.** Create a random secret key that will be used to sign the JWT tokens.
To generate a secure random secret key use the command:
```openssl rand -hex 32```

Example of secret key:
"09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7".

**4.** Open the project folder and create .env file with the following environmental variables:
```commandline
POSTGRES_USER="<user>"
POSTGRES_PASSWORD="<password>"
POSTGRES_DB="<postgres_db>"
POSTGRES_HOST="tg_collector_db"
SECRET_KEY="<your_secret_ket>"
TG_BOT_TOKEN="<your_bot_token>"
WEBHOOK_HOST="<your_host>"
WEBHOOK_PATH="/messages/"
```
You can choose any values for variables POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

Paste TG_BOT_TOKEN from step 1 and SECRET_KEY from step 2.

WEBHOOK_HOST is a name of your server with this app. 
For test launching on your local PC, you may install ngrok (from https://ngrok.com/) 
and use command ```ngrok http 8000``` to get external link (example: "https://f7f0-37-252-81-208.eu.ngrok.io") 

You also may add variables ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM and POSTGRES_PORT.
They have default values 60, "HS256" and 5432 respectively.

**5A.** Run it with Docker-compose:
- Install Docker Compose
  (https://docs.docker.com/compose/install/)
- Run all containers with ```docker-compose up -d```

**5B.** Test launching with SQLite (instead of 5A):
- Install Python if required
  (https://www.python.org/downloads/)
-  Create a virtual environment in the project folder: ```python -m venv env``` 
  (or use command “python3” here and below, if “python” doesn’t work)
- Activate the virtual environment: 

  ```env\Scripts\activate``` (for Windows) 

  ```source env/bin/activate``` (for Linux/Mac) 
- Run ```pip install -r requirements.txt```
- Open main.py, comment line 23 ```db_url=settings.postgresql_url,```, 
  uncomment line 24 ```db_url="sqlite://database/db.sqlite",``` and save it
- Start app with ```python main.py```
___
## How to use
- Open http://127.0.0.1:8000/ to check REST API
- See automatically generated documentation by Swagger http://127.0.0.1:8000/docs
- Create new user and log in.
- Add bot in Telegram chats, give it access to chat messages
- You can see allowed commands in the bot menu or with command ```/start```
- Try to use FSM with command ```/rate```

___
## Where it can be used
This application is a versatile tool that can be used in a variety of scenarios to improve communication and streamline message management from Telegram chats. 
Here are some examples:

Customer Support: 

Companies can collect and manage customer queries and complaints from Telegram chats. 
Administrators can access the REST service to view and manage the messages, monitor active chats, and provide prompt responses to customers.

Social Media Management: 

Social media managers can collect and manage comments and messages from their organization's social media channels on Telegram. 
This helps them to streamline their social media management efforts and respond to inquiries in a timely manner.

Event Management: 

This app can be used to collect and manage messages from Telegram groups created for events. 
Event organizers can use the application to monitor the group's activity, respond to inquiries, and keep participants informed about updates and changes.

Collaborative Projects: 

Teams working on collaborative projects can manage communication and collect feedback from Telegram groups. 
The REST service provides easy access to messages and chats.



