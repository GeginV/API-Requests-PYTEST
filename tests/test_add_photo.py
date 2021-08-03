"""FIXME"""
#figure out how to test the request

import os.path

import pytest

from api import PetFriends
from settings import valid_email, valid_password, valid_pet_id

pf = PetFriends()

class TestPositive:
    pass

    @pytest.fixture()
    def get_valid_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert  status == 200
        assert 'key' in self.key

        yield

        assert status == 200

