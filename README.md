# User Service

## Description

User Service is a microservice for user management built using FastAPI, PostgreSQL, Redis, and RabbitMQ.

## Requirements

- Python 3.10
- PostgreSQL
- Redis
- RabbitMQ
- Docker (for running RabbitMQ)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Eastwesser/candy-star.git
    cd candy-star/backend/user-service
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create and configure the `.env` file based on `.env.example`:

    ```sh
    cp .env.example .env
    ```

## Starting Services

### PostgreSQL

Ensure PostgreSQL is installed and running. Configure the connection in the `.env` file.

### Redis

Install and start the Redis server:
   ```sh
   # On Ubuntu
   sudo apt update
   sudo apt install redis-server
   sudo systemctl start redis-server
   sudo systemctl status redis-server
   ```

Check the status of Redis:
   ```
   sudo systemctl status redis-server
   ```

### RabbitMQ

Start RabbitMQ using Docker:
   ```
   docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

### Running the Application

Start the application:
   ```
   uvicorn app.main:app --reload
   ```

The application will be available at http://127.0.0.1:8001.

API documentation will be available at http://127.0.0.1:8001/docs.

### Project Structure
   ```
   user-service/
   ├── app/
   │ ├── __init__.py
   │ ├── main.py
   │ ├── db/
   │ │ ├── __init__.py
   │ │ ├── session.py
   │ ├── models/
   │ │ ├── __init__.py
   │ │ ├── user.py
   │ ├── routers/
   │ │ ├── __init__.py
   │ │ ├── user.py
   │ └── schemas/
   │ ├── __init__.py
   │ ├── user.py
   ├── .env
   ├── .env.example
   ├── requirements.txt
   └── README.md
   ```

### API Request Examples

Get All Users
   ```
   GET /users
   ```
Create a New User
   ```
   POST /users
   {
   "username": "john_doe",
   "email": "john.doe@example.com",
   "password": "securepassword"
   }
   ```

### Contact

For questions and suggestions:

Me - eastwesser@gmail.com

GitHub - https://github.com/Eastwesser

© 2024 Candy-Star. All rights reserved.
