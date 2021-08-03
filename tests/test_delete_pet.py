"""FIXME"""
#figure out how to make it accept bad keys

import pytest

from api import PetFriends
from settings import valid_email, valid_password, unlisted_pet_ID,\
    broken_key, key_of_different_user, valid_pet_id

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

    def test_delete_pet(self, get_valid_key):
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        if len(my_pets) == 0:
            self.pf.add_new_pet(self.key, 'leCat', 'cat', "3", 'images/cat.jpeg')
            _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        pet_id = my_pets['pets'][0]['id']

        status, _ = self.pf.delete_pet(self.key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        assert pet_id not in my_pets.values()


#figure out how to make it accept bad keys
@pytest.mark.skip(reason='impossible to run without a valid key ')
@pytest.mark.parametrize("auth_key", [broken_key, key_of_different_user, ''],
                         ids=["BROKEN KEY", "SOMEBODY'S KEY", "EMPTY"])
@pytest.mark.parametrize('pet_id', [valid_pet_id, unlisted_pet_ID, ''],
                         ids=["VALID PET", "UNLISTED PET", "EMPTY"])
def test_delete_pet_invalid(auth_key, pet_id):
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert pet_id not in my_pets.values()
    assert status == 400
