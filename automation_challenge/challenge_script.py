from datetime import datetime
import json
import requests

BASE_URL = 'https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app'
TOKEN = "fFz8Z7OpPTSY7gpAFPrWntoMuo07ACjp"
USERNAME = "datacose"
PASSWORD = "196D1115456D7"


def get_people():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/people/", headers=headers) 
    return json.loads(response.content)


def person_to_contact(person_object):
    person = person_object["fields"]
    birthdate = datetime.strptime(person["dateOfBirth"], '%d-%m-%Y').date().strftime('%Y-%m-%d')
    return {
        "first_name": person['firstName'].strip(),
        "last_name": person['lastName'].strip(),
        "birthdate": birthdate,
        "email": person['email'],
        "custom_properties": {
            "airtable_id": person_object['id'],
            "lifetime_value": float(person['lifetime_value'][1:])
        }
    }

def people_to_contacts(people_data):
    contact_data = []
    for person_object in people_data:
        contact_data.append(person_to_contact(person_object))
    return contact_data


def push_contacts(contacts):
    for contact in contacts:
        response = requests.post(f"{BASE_URL}/contacts/", auth=(USERNAME, PASSWORD), json=contact, timeout=5)
        if response.status_code != 200:
            return False
    return True
    
def main():
    people_data = get_people()
    contacts = people_to_contacts(people_data)
    status = push_contacts(contacts)
    if status:
        print("Transaction Completed Successfully!")
    else:
        print("Transaction Failed!")
    

if __name__ == "__main__":
    main()