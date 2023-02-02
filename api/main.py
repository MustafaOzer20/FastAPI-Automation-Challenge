import secrets
from typing import List
from fastapi import Depends, FastAPI, Header, Request, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from models import ContactCreate, Person, Contact, PersonFields, CustomProperties
import datetime
from uuid import uuid4
from fastapi.responses import PlainTextResponse


app = FastAPI()

### Token ###
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="fFz8Z7OpPTSY7gpAFPrWntoMuo07ACjp")
security = HTTPBasic(auto_error=False)
#############

### Fake DB ###
person_db:List[Person] = []
contact_db:List[Contact] = []
###################

@app.get("/people", description="Get People")
async def get_people(token: str = Depends(oauth2_scheme)) -> List[Person]:
    return person_db

def get_user(username, password):
    with open("LOGIN") as f:
        _username = f.readline()
    with open("PASSWORD") as f:
        _password = f.readline()
    return secrets.compare_digest(username, _username) and secrets.compare_digest(password, _password)

@app.post("/contacts", description="Create Contact")
async def create_contact(contact:ContactCreate, request: Request, credentials: HTTPBasicCredentials = Depends(security)) -> Contact:
    ### API Basic Auth ###
    username = credentials.username if credentials else ''
    password = credentials.password if credentials else ''
    if not get_user(username, password):
        return PlainTextResponse("{}", status_code=401)
    ############################

    ### Data Cleaning Needed ###
    contact.first_name = contact.first_name.strip()
    contact.last_name = contact.last_name.strip()
    ############################

    ### Contact Add ###
    new_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name, 
        birthdate=contact.birthdate, 
        email=contact.email, 
        custom_properties=contact.custom_properties
    )
    contact_db.append(new_contact)
    ###################

    ### Person Add ###
    person = Person(
        id=str(uuid4()), 
        fields=PersonFields(
            id=str(uuid4()), 
            firstName=contact.first_name, 
            lastName=contact.last_name, 
            dateOfBirth=contact.birthdate, 
            email=contact.email, 
            lifetime_value="$"+str(contact.custom_properties.lifetime_value)
        )
    )
    person_db.append(person)
    ###################
    return new_contact
