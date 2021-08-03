import os.path

import pytest

from api import PetFriends
from settings import valid_email, valid_password
pf = PetFriends()


class TestPositive:
    pass

    @pytest.fixture(autouse=True)
    def get_valid_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert status == 200

    @pytest.mark.WITH_PHOTO
    @pytest.mark.parametrize('name', ["Pet", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID NAME', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("animal_type", ["Cat", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID TYPE', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("age", ['1'], ids=['MINIMAL AGE'])
    def test_add_new_pet_valid_data(self, name, animal_type, age, pet_photo='images/cat.jpeg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age

    @pytest.mark.NO_PHOTO
    @pytest.mark.parametrize('name', ["Pet", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID NAME', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("animal_type", ["Cat", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID TYPE', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("age", ['1'], ids=['MINIMAL AGE'])
    def test_create_pet_simple_valid_data(self, name, animal_type, age):
        status, result = self.pf.create_pet_simple(self.key, name, animal_type, age)
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age


class TestNegative:
    pass

    @pytest.fixture(autouse=True)
    def get_valid_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert status == 400

    @pytest.mark.WITH_PHOTO
    @pytest.mark.parametrize('name', [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("animal_type",  [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("age", ["Cat", "Пытомыц", '共产党宣言', '', '-1', '0', '1.23', '100', '1'*255, '1'*10000],
                             ids=['VALID TYPE', "RUSSIAN", "CHINESE", "EMPTY STRING", "NEGATIVE", "ZERO", "FLOAT",
                                  "TOO OLD" "255 CHARACTERS", "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize('pet_photo', ["", "images/cat.pdf"], ids=["NO FILE", "WRONG FORMAT"])
    def test_add_new_pet_invalid_data(self, name, age, animal_type, pet_photo):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)
        assert ['name'] not in result
        assert ['age'] not in result
        assert ['animal_type'] not in result

    @pytest.mark.NO_PHOTO
    @pytest.mark.parametrize('name', [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("animal_type", [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("age", ["Cat", "Пытомыц", '共产党宣言', '', '-1', '0', '1.23', '100', '1' * 255, '1' * 10000],
                             ids=['VALID TYPE', "RUSSIAN", "CHINESE", "EMPTY STRING", "NEGATIVE", "ZERO", "FLOAT",
                                  "TOO OLD" "255 CHARACTERS", "10K CHARACTERS", "SYMBOLS"])
    def test_create_pet_simple_invalid_data(self, name, animal_type, age):
        status, result = self.pf.create_pet_simple(self.key, name, animal_type, age)
        assert ['name'] not in result
        assert ['age'] not in result
        assert ['animal_type'] not in result
