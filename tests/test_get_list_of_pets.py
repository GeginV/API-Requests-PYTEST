"""FIXME"""
#figure out how to make it take bad keys

import pytest

from api import PetFriends
from settings import valid_email, valid_password, \
    wrong_password, wrong_email, unlisted_pet_ID, \
    broken_key, key_of_different_user

pf = PetFriends()

class TestPositive():
    pass

    @pytest.fixture(autouse=True)
    def get_valid_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert  status == 200
        assert 'key' in self.key

        yield

        assert status == 200

    @pytest.mark.parametrize("filter", ['', "my_pets"], ids= ["EMPTY FILER", "MY_PETS"])
    def test_get_all_pets_with_valid_key(self, filter):  # filter available values : my_pets
        status, result = self.pf.get_list_of_pets(self.key, filter)
        assert len(result['pets']) > 0

@pytest.mark.skip(reason='impossible run it without a valid key')
@pytest.mark.parametrize("auth_key", [broken_key, key_of_different_user, ''],
                         ids=["BROKEN KEY", "SOMEBODY'S KEY", "EMPTY"])
@pytest.mark.parametrize("filter", ['', "my_pets"],
                         ids= ["EMPTY FILER", "MY_PETS"])
def test_get_all_pets_invalid_key( auth_key, filter):  # filter available values : my_pets
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert len(result['pets']) not in result
    assert status == 400