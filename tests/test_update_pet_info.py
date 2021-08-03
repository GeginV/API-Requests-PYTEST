import pytest

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


class TestPositive:
    pass

    @pytest.fixture()
    def get_valid_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert status == 200

    @pytest.mark.parametrize('name', ["Pet", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID NAME', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("animal_type", ["Cat", "123", "Пытомыц", '共产党宣言', 'a'*255, 'a'*100000, '!#$%@$'],
                             ids=['VALID TYPE', "NUMBERS", "RUSSIAN", "CHINESE", "255 CHARACTERS",
                                  "10K CHARACTERS", "SYMBOLS"])
    @pytest.mark.parametrize("age", ['1'], ids=['MINIMAL AGE'])
    def test_update_pet_info_valid_data(self, name, animal_type, age):
        _, my_pets = self.pf.get_list_of_pets(self.key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert result['name'] == name
            assert result['animal_type'] == animal_type
            assert result['age'] == age
        else:
            raise Exception('No pets found')


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

    @pytest.mark.parametrize('name', [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("animal_type", [""], ids=['EMPTY STRING'])
    @pytest.mark.parametrize("age", ["Cat", "Пытомыц", '共产党宣言', '', '-1', '0', '1.23', '100', '1' * 255, '1' * 10000],
                             ids=['VALID TYPE', "RUSSIAN", "CHINESE", "EMPTY STRING", "NEGATIVE", "ZERO", "FLOAT",
                                  "TOO OLD" "255 CHARACTERS", "10K CHARACTERS", "SYMBOLS"])
    def test_update_pet_info_invalid_data(self, name, animal_type, age):
        _, my_pets = self.pf.get_list_of_pets(self.key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert result['name'] == name
            assert result['animal_type'] == animal_type
            assert result['age'] == age
        else:
            raise Exception('No pets found')
