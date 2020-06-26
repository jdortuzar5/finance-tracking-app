from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
import uuid
from typing import List, Optional
import uvicorn
from bson import json_util
from datetime import datetime
from datetime import date
import os

MONGO_HOST = os.getenv("MONGOHOST")
# Database Model definitions

class Category(BaseModel):
    user_uuid: str
    name: str

class User(BaseModel):
    username: str
    email: str
    name: str
    uuid: str
    password: str

class Income(BaseModel):
    user_uuid: str
    amount: float
    currency: str
    date: str
    categories: Optional[Category]

    @validator("date")
    def only_date_validator(cls, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

class Spending(BaseModel):
    user_uuid: str
    amount: float
    currency: str
    date: str
    categories: Optional[Category]

    @validator("date")
    def only_date_validator(cls, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

# Connecting to DataBase (Mongo Client)
client = MongoClient(MONGO_HOST, 27017)
db = client["finantial-tracker"]

user_col = db["Users"]
income_col = db["Income"]
spend_col = db["Spendings"]
category_col = db["Categoriies"]

# Defining Backend

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://0.0.0.0:5000",
    "http://593c8752712e.ngrok.io/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Async Auxiliary Functions

async def find_income_by_user(user):
    income_gen = income_col.find({"user_uuid": user})
    income_list = [json_util.dumps(income) for income in income_gen]
    return income_list

async def find_spending_by_user(user):
    spending_gen = spend_col.find({"user_uuid": user})
    spending_list = [json_util.dumps(spending) for spending in spending_gen]
    return spending_list

def user_exist(user):
    user_one = user_col.find_one({"uuid": user})
    if user_one is not None:
        return True
    else:
        return False

def new_user_exist(username, email, name):
    user_one = user_col.find_one({"username": username})
    if user_one is not None:
        return True
    else:
        user_one = user_col.find_one({"email": email})
        if user_one is not None:
            return True
        else:
            return False

async def create_user_in_DB(username: str, email: str, name: str, password: str):
    new_user_uuid = str(uuid.uuid4())
    new_user = User(username=username,
                    email=email,
                    name=name,
                    uuid=new_user_uuid,
                    password=password)
    user_col.insert_one(new_user.dict())
    return True

async def create_new_income(income):
    income_col.insert_one(income.dict())
    return True

async def create_new_spending(spending):
    spend_col.insert_one(spending.dict())
    return True

# Income CRUD Endpoints

@app.get("/{user}/income", tags=["Income"])
async def get_income_by_user(user: str):
    """
    This function return an array with all the income documents
    created by the User. In case the user is not found, raises an error
    message while returning 200.

    user: user uuid
    """
    user_bool = user_exist(user)
    if user_bool: 
        incomes = await find_income_by_user(user)
        return {"Message": "sucessful", "payload": incomes}
    else:
        return {"Message": "error", "payload": "User not found."}

@app.post("/{user}/new_income", tags=["Income"])
async def post_user_income(user: str, income: Income):
    """
    This functions create a new income in the DB. It checks whether
    the user exists and returns a message in case no user exists. 
    In the other case, creates a new document in DB with the users
    new Income.
    user: users uuid.
    income: Income (check pyndatic model) parameters to save in DB.
    """

    user_bool = user_exist(user)
    if user_bool:
        income_created = await create_new_income(income)
        if income_created:
            return {"Message": "sucesful", "payload": "Income creates sucessfully."}
        else:
            return {"Message": "error", "payload": "There was an error creating Income."}
    else:
        return {"Message": "error", "payload": "User not found."}

@app.post("/{user}/delete_income", tags=["Income"])
async def delete_income(user: str, income: Income):
    """
    This endpoints delete an income if the Users want to delete an income from the DB.
    user: users uuid
    income: the Income model that is going to be deleted.
    """
    income_dict = income.dict()
    income_col.delete_one({"user_uuid": income_dict["user_uuid"], 
                           "amount": income_dict["amount"],
                           "currency": income_dict["currency"],
                           "categories": income_dict["categories"]})
    
    return {"Message": "sucessful", "payload": "Income deleted."}


# User CRUD endpoints 

@app.post("/create_user", tags=["User"])
async def create_user(username: str, email: str, name: str, password: str):
    """
    This function creates a new User in the DB. It checks whether 
    the parameters for the user already exist in the DB and returns
    an error message if User exists. In case there no User with
    input parameters, a new User document is created in the DB.

    username: string with the Users username.
    email: string with the User email (type verified by frontend).
    name: string with the Users name, can be First or Full name.
    """
    new_user_bool = new_user_exist(username, email, name)
    if new_user_bool:
        return {"Message": "error", "payload": "User already exist."}
    else:
        user_created = await create_user_in_DB(username, email, name, password)

        if user_created:
            return {"Message": "sucessful", "payload": "User created succesfully."}
        else:
            return {"Message": "error", "payload": "There was an error creating User."}

@app.get("/{email}/get_id", tags=["User"])
async def get_user_id(email: str, password: str):
    """
    This function is used for geting the uuid for a User.
    """
    user = user_col.find_one({"password": password, "email": email})
    user_id = user["uuid"]
    return {"Message": "sucessful", "payload": user_id}


# Spending CRUD endpoints

@app.get("/{user}/spending", tags=["Spendings"])
async def get_spendings_by_user(user: str):
    """
    This function return an array with all the income documents
    created by the User. In case the user is not found, raises an error
    message while returning 200.

    user: user uuid
    """
    user_bool = user_exist(user)
    if user_bool: 
        incomes = await find_spending_by_user(user)
        return {"Message": "sucessful", "payload": incomes}
    else:
        return {"Message": "error", "payload": "User not found."}

@app.post("/{user}/new_spending", tags=["Spendings"])
async def post_user_spending(user: str, spending: Spending):
    """
    This function creates a new spending document for the User.
    """
    user_bool = user_exist(user)
    if user_bool:
        spending_created = await create_new_spending(spending)
        if spending_created:
            return {"Message": "sucesful", "payload": "Income creates sucessfully."}
        else:
            return {"Message": "error", "payload": "There was an error creating Income."}
    else:
        return {"Message": "error", "payload": "User not found."}

@app.post("/{user}/delete_spending", tags=["Spendings"])
async def delete_spending(user: str, spending: Spending):
    """
    This function deletes a spending.
    """
    spending_dict = spending.dict()
    spend_col.delete_one({"user_uuid": spending_dict["user_uuid"], 
                           "amount": spending_dict["amount"],
                           "currency": spending_dict["currency"],
                           "categories": spending_dict["categories"]})
    
    return {"Message": "sucessful", "payload": "Spending deleted."}

# Graphs endpoints

@app.get("/{user}/income/time_series", tags=["Graphs"])
async def get_income_time_series(user):
    user_income = await find_income_by_user(user)
    date_list = list(set([datetime.strptime(json_util.loads(spending)["date"],"%Y-%m-%d") for spending in user_income]))
    date_list = sorted(date_list)
    date_list = [date.strftime("%Y-%m") for date in date_list]
    graph_dict = {}
    new_date_list = []
    value_list = []
    for date in date_list:
        graph_dict[date] = 0
        for income in user_income:
            if date in json_util.loads(income)["date"]:
                graph_dict[date] += json_util.loads(income)["amount"]

    for date, value in graph_dict.items():
        new_date_list.append(date)
        value_list.append(value)
    graph_dict = {"labels": list(set(date_list)), "values": value_list}
    return graph_dict

@app.get("/{user}/spending/time_series", tags=["Graphs"])
async def get_spending_time_series(user):
    user_spending = await find_spending_by_user(user)
    date_list = list(set([datetime.strptime(json_util.loads(spending)["date"],"%Y-%m-%d") for spending in user_spending]))
    date_list = sorted(date_list)
    date_list = [date.strftime("%Y-%m") for date in date_list]
    graph_dict = {}
    new_date_list = []
    value_list = []
    for date in date_list:
        graph_dict[date] = 0
        for spending in user_spending:
            if date in json_util.loads(spending)["date"]:
                graph_dict[date] += json_util.loads(spending)["amount"]

    for date, value in graph_dict.items():
        new_date_list.append(date)
        value_list.append(value)
    graph_dict = {"labels": list(set(date_list)), "values": value_list}
    return graph_dict



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", debug=True)