import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        '''method sends an API quarry that gets status code and json response with individual user key that corresponds
         user's email and password '''

        headers = {'email': email,
                   'password': password
                   }

        res = requests.get(self.base_url+'api/key',  headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        '''method that adds a new pet without a photo returning status code  and a JSON with a successfully
         created pet'''
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'age': age,
                'animal_type': animal_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        '''Method that sends data to the server to add a pet, it's name, age, type and image. As response it gets
        a JSON with new pet data'''

        data = MultipartEncoder(
            fields={'name': name,
                    'animal type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = ''):
        '''method that uses the received key to access the list of all pets'''

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        '''Method that sends a quarry to update a pet with corresponding ID returning status code and a JSON with
        updated pet info'''

        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'age': age,
                'animal_type': animal_type}

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        '''method that allows to upload a photo in a pet profile with a corresponding pet ID returning a JSON with
        "pet_photo" parameter included if successful'''
        headers = {'auth_key': auth_key}
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')})

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        '''Method that sends a quarry to delete a pet with a corresponding ID returning a JSON that confirms if deletion
        was a success. The known issue is that the object "result" is an empty string however the status is 200 '''

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
