import pytest

from api import PetFriends
from settings import valid_email, valid_password, \
    wrong_password, wrong_email

pf = PetFriends()


@pytest.mark.key_positive
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


@pytest.mark.key_negative
@pytest.mark.parametrize("email", [wrong_email, 'I am email', '', 'Почта', 240, '共产党宣言', 'a'*255, 'a'*100000,
                                   None, True],
                         ids=['unregistered user', 'not an email', 'empty string', 'Russian', 'number', 'Chinese',
                              'maximum sting', 'abysmal string', 'none', 'boolean'])
@pytest.mark.parametrize("password", [wrong_password, 'I am password', '', 'Пароль', 320, '共产党宣言', 'a'*255, 'a'*100000,
                                      None, True],
                         ids=['unregistered password', 'not a password', 'empty string', 'Russian', 'number', 'Chinese',
                              'maximum sting', 'abysmal string', 'none', 'boolean'])
def test_get_key_invalid_data(email, password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
