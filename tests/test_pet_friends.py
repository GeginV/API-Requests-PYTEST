import os.path

from api import PetFriends
from settings import valid_email, valid_password, \
    wrong_password, wrong_email, unlisted_pet_ID, \
    broken_key, key_of_different_user

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_email(email=wrong_email, password=valid_password):
    '''my'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password=wrong_password):
    '''my'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_none (email=None, password=None):
    '''my'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_not_email (email='give key pls', password=wrong_password):
    '''my'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Doomed', animal_type='Cat', age='99', pet_photo='images/cat.jpeg'):
    '''FIXME'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_unexpected_info(name=123, animal_type={'a': 'cat'}, age='old', pet_photo='images/cat.jpeg'):
    '''FIXME'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200

def test_add_new_pet_with_invalid_file_format(name='Doomed', animal_type='Cat', age=4, pet_photo='images/cat.pdf'):
    '''FIXME'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200

def test_create_pet_simple_with_valid_data(name='Doomed', animal_type='Cat', age=4):
    '''my'''
    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert  result['name'] == name

def test_create_pet_simple_with_unexpected_info(name=123, animal_type={'a': 'cat'}, age='old'):
    '''my'''
    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_create_pet_simple_with_long_name(name='lo' + 'o'*1000000 +'ng', animal_type='cat', age=2):
    """my"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] ==name

def test_create_pet_simple_with_none(name=None, animal_type=None, age=None):
    """my"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

def test_create_pet_simple_with_booleans(name = True, animal_type = False, age = True):
    '''my'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_with_empty_info(name='', animal_type='', age=''):
    '''my'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets) == 0:
        pf.add_new_pet(auth_key, 'leCat', 'cat', 3, 'images/cat.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_unlisted_pet(pet_id=unlisted_pet_ID):
    '''my'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200

def test_successful_update_self_pet_info(name='Cat Eater', animal_type='Fish', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert  status == 200
        assert result['name'] == name
    else:
        raise Exception('No pets found')

