from unittest import TestCase
from challenge_script import get_people, people_to_contacts, person_to_contact, push_contacts


class ChallengeTests(TestCase):

    def test_get_people(self):
        all_data: list = get_people()
        sample_data = {
            "id": "rec132457689",
            "fields": {
                "firstName": "John",
                "lastName": "Doe",
                "dateOfBirth": "31-01-1973",
                "email": "john@example.co",
                "lifetime_value": "$229.00"
            }
        }
        self.assertEqual(all_data.pop(), sample_data)

    def test_person_to_contact(self):
        all_data:list = get_people()
        person = all_data.pop()
        contact = person_to_contact(person)
        sample_data = {
            'first_name': 'John',
            'last_name': 'Doe', 
            'birthdate': '1973-01-31',
            'email': 'john@example.co', 
            'custom_properties': {
                'airtable_id': 'rec132457689', 
                'lifetime_value': 229.0
            }
        }
        self.assertEqual(contact, sample_data)

    def test_people_to_contacts(self):
        all_data:list = get_people()
        contacts:list = people_to_contacts(all_data)
        sample_data = {
            'first_name': 'John',
            'last_name': 'Doe', 
            'birthdate': '1973-01-31',
            'email': 'john@example.co', 
            'custom_properties': {
                'airtable_id': 'rec132457689', 
                'lifetime_value': 229.0
            }
        }
        self.assertEqual(contacts.pop(), sample_data)

    def test_push_contacts_success(self):
        people_data = get_people()
        contacts = people_to_contacts(people_data)
        self.assertEqual(push_contacts(contacts), True)
    
    def test_push_contacts_failed(self):
        sample_data = [
            {
                'first_name': 'James',
                'last_name': 'Larry', 
                'birthdate': '31-01-1986', 
                'email': 'jlarry@example.co', 
                'custom_properties': {
                    'airtable_id': 'rec123456789', 
                    'lifetime_value': "125500.00"
                }
            }
        ]
        self.assertEqual(push_contacts(sample_data), False)


    
