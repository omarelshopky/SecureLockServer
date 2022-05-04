# Secure Lock Server

An authentication system uses flask-jwt-extended for APIs used in the flatter app.

<br>

## Establish the app

- Create a virtual environment with all required dependencies by running those commands

```sh
pip install pipenv
pipenv install
```

- Set your environment variables in **.env** file
- Then start the flask app by

```sh
pipenv shell
flask run
```

## Update the Database

- If you do any change in the database models run this code to update the schema

```py
from main import db, app
db.create_all(app=app)
```

<br>

## Endpoints Usage

### /register

- Register a new user in the database
  
**Request Body**

```json
{
    "username"  : "USER_USERNAME",
    "password"  : "USER_PASSWORD",
    "email"     : "USER_EMAIL",
    "phone"     : "USER_PHONE",
    "address"   : "USER_ADDRESS"
}
```

**Response**

- Registered Successfully

```json
{
    "msg": "User registered successfully"
}
```

- User Exist in the Database

```json
{
    "msg": "User already exists"
}
```

- Password less than 8 characters

```json
{
    "msg": "Weak password"
}
```

- Exceed Ratelimit

```json
{
    "error": "ratelimit exceeded"
}
```

### /login

- Login with a specific user already in the database
  
**Request Body**

```json
{
    "username" : "YOUR_USERNAME",
    "password" : "YOUR_PASSWORD"
}
```

**Response**

- Login Successfully

```json
{
    "access_token": "YOUR_JWT_TOKEN"
}
```

- Wrong Credentials

```json
{
    "msg": "Invalid username or password"
}
```

- Exceed Ratelimit

```json
{
    "error": "ratelimit exceeded"
}
```

### /logUnlocking

- Log unlocking process done with specific client
  
**Request Header**

```json
headers = {
  "Authorization": "Bearer <JWT_TOKEN>"
}
```

**Request Body**

```json
{
    "unlocking-method" : "HOW_CLIENT_UNLOCK"
}
```

**Response**

- Authorized User to log his/her unlocking

```json
{
    "msg": "Unlocking process logged successfully"
}
```

- Token Error

```json
{
    "msg": "There is an error with this token"
}
```

- Exceed Ratelimit

```json
{
    "error": "ratelimit exceeded"
}
```

## Debugging Endpoints

> *reach them directly from browser*

### /getLogs

- Returns all logs datat stored in the database

### /getUsers

- Returns all users datat stored in the database
