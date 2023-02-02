from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4
import datetime

class CustomProperties(BaseModel):
    airtable_id:str
    lifetime_value:float

class ContactCreate(BaseModel):
    first_name:str
    last_name:str
    birthdate:datetime.date
    email:str
    custom_properties:CustomProperties

class Contact(BaseModel):
    first_name:str
    last_name:str
    birthdate:datetime.date
    email:str
    custom_properties:CustomProperties
    id:Optional[UUID] = uuid4()
    

class PersonFields(BaseModel):
    firstName:str
    lastName:str
    dateOfBirth:datetime.date
    email:str
    lifetime_value:str
    id: str


class Person(BaseModel):
    id: str
    fields:PersonFields


class User(BaseModel):
    username: str
    password: str


