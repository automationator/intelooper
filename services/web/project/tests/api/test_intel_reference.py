import json

from project.tests.conftest import TEST_ANALYST_APIKEY, TEST_INACTIVE_APIKEY, TEST_INVALID_APIKEY
from project.tests.helpers import *


"""
CREATE TESTS
"""


def test_create_missing_parameter(client):
    """ Ensure the required parameters are given """

    data = {'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['message'] == 'Request must include: reference, source, username'

    data = {'username': 'analyst', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['message'] == 'Request must include: reference, source, username'

    data = {'username': 'analyst', 'reference': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['message'] == 'Request must include: reference, source, username'


def test_create_duplicate(client):
    """ Ensure a duplicate record cannot be created """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['message'] == 'Intel reference already exists'


def test_create_nonexistent_source(client):
    """ Ensure a reference cannot be created with a nonexistent source """

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['message'] == 'Intel source not found'


def test_create_missing_api_key(app, client):
    """ Ensure an API key is given if the config requires it """

    app.config['POST'] = 'analyst'

    data = {'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Bad or missing API key'


def test_create_invalid_api_key(app, client):
    """ Ensure an API key not found in the database does not work """

    app.config['POST'] = 'analyst'

    data = {'apikey': TEST_INVALID_APIKEY, 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user does not exist'


def test_create_inactive_api_key(app, client):
    """ Ensure an inactive API key does not work """

    app.config['POST'] = 'analyst'

    data = {'apikey': TEST_INACTIVE_APIKEY, 'name': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user is not active'


def test_create_invalid_role(app, client):
    """ Ensure the given API key has the proper role access """

    app.config['POST'] = 'user_does_not_have_this_role'

    data = {'apikey': TEST_ANALYST_APIKEY, 'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Insufficient privileges'


def test_create(client):
    """ Ensure a proper request actually works """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    assert request.status_code == 201


"""
READ TESTS
"""


def test_read_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    request = client.get('/api/intel/reference/100000')
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['message'] == 'Intel reference ID not found'


def test_read_missing_api_key(app, client):
    """ Ensure an API key is given if the config requires it """

    app.config['GET'] = 'analyst'

    request = client.get('/api/intel/reference/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Bad or missing API key'


def test_read_invalid_api_key(app, client):
    """ Ensure an API key not found in the database does not work """

    app.config['GET'] = 'analyst'

    request = client.get('/api/intel/reference/1?apikey={}'.format(TEST_INVALID_APIKEY))
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user does not exist'


def test_read_inactive_api_key(app, client):
    """ Ensure an inactive API key does not work """

    app.config['GET'] = 'analyst'

    request = client.get('/api/intel/reference/1?apikey={}'.format(TEST_INACTIVE_APIKEY))
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user is not active'


def test_read_invalid_role(app, client):
    """ Ensure the given API key has the proper role access """

    app.config['GET'] = 'user_does_not_have_this_role'

    request = client.get('/api/intel/reference/1?apikey={}'.format(TEST_ANALYST_APIKEY))
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Insufficient privileges'


def test_read_all_values(client):
    """ Ensure all values properly return """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf2', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf3', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    assert request.status_code == 201

    request = client.get('/api/intel/reference')
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert len(response) == 3


def test_read_by_id(client):
    """ Ensure names can be read by their ID """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    request = client.get('/api/intel/reference/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['reference'] == 'asdf'


"""
UPDATE TESTS
"""


def test_update_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    data = {'reference': 'asdf', 'source': 'asdf'}
    request = client.put('/api/intel/reference/100000', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['message'] == 'Intel reference ID not found'


def test_update_missing_parameter(client):
    """ Ensure the required parameters are given """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    request = client.put('/api/intel/reference/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['message'] == 'Request must include at least reference or source'


def test_update_duplicate(client):
    """ Ensure duplicate records cannot be updated """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.put('/api/intel/reference/{}'.format(_id), data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['message'] == 'Intel reference already exists'


def test_update_nonexistent_source(client):
    """ Ensure a reference cannot be updated with a nonexistent source """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    data = {'source': 'asdf2'}
    request = client.put('/api/intel/reference/{}'.format(_id), data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['message'] == 'Intel source not found'


def test_update_missing_api_key(app, client):
    """ Ensure an API key is given if the config requires it """

    app.config['PUT'] = 'analyst'

    data = {'reference': 'asdf', 'source': 'asdf'}
    request = client.put('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Bad or missing API key'


def test_update_invalid_api_key(app, client):
    """ Ensure an API key not found in the database does not work """

    app.config['PUT'] = 'analyst'

    data = {'apikey': TEST_INVALID_APIKEY, 'reference': 'asdf', 'source': 'asdf'}
    request = client.put('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user does not exist'


def test_update_inactive_api_key(app, client):
    """ Ensure an inactive API key does not work """

    app.config['PUT'] = 'analyst'

    data = {'apikey': TEST_INACTIVE_APIKEY, 'name': 'asdf'}
    request = client.put('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user is not active'


def test_update_invalid_role(app, client):
    """ Ensure the given API key has the proper role access """

    app.config['PUT'] = 'user_does_not_have_this_role'

    data = {'apikey': TEST_ANALYST_APIKEY, 'reference': 'asdf', 'source': 'asdf'}
    request = client.put('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Insufficient privileges'


def test_update(client):
    """ Ensure a proper request actually works """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    data = {'reference': 'asdf2'}
    request = client.put('/api/intel/reference/{}'.format(_id), data=data)
    assert request.status_code == 200

    request = client.get('/api/intel/reference/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response['id'] == _id
    assert response['reference'] == 'asdf2'


"""
DELETE TESTS
"""


def test_delete_nonexistent_id(client):
    """ Ensure a nonexistent ID does not work """

    request = client.delete('/api/intel/reference/100000')
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['message'] == 'Intel reference ID not found'


def test_delete_missing_api_key(app, client):
    """ Ensure an API key is given if the config requires it """

    app.config['DELETE'] = 'admin'

    request = client.delete('/api/intel/reference/1')
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Bad or missing API key'


def test_delete_invalid_api_key(app, client):
    """ Ensure an API key not found in the database does not work """

    app.config['DELETE'] = 'admin'

    data = {'apikey': TEST_INVALID_APIKEY}
    request = client.delete('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user does not exist'
    
    
def test_delete_inactive_api_key(app, client):
    """ Ensure an inactive API key does not work """

    app.config['DELETE'] = 'admin'

    data = {'apikey': TEST_INACTIVE_APIKEY}
    request = client.delete('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'API user is not active'


def test_delete_invalid_role(app, client):
    """ Ensure the given API key has the proper role access """

    app.config['DELETE'] = 'user_does_not_have_this_role'

    data = {'apikey': TEST_ANALYST_APIKEY}
    request = client.delete('/api/intel/reference/1', data=data)
    response = json.loads(request.data.decode())
    assert request.status_code == 401
    assert response['message'] == 'Insufficient privileges'


def test_delete_foreign_key_event(client):
    """ Ensure you cannot delete with foreign key constraints """

    reference_request, reference_response = create_intel_reference(client, 'analyst', 'OSINT', 'http://blahblah.com')
    event_request, event_response = create_event(client, 'test_event', 'analyst', TEST_ANALYST_APIKEY, intel_reference='http://blahblah.com', intel_source='OSINT')
    assert reference_request.status_code == 201
    assert event_request.status_code == 201

    request = client.delete('/api/intel/reference/{}'.format(reference_response['id']))
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['message'] == 'Unable to delete intel reference due to foreign key constraints'


def test_delete_foreign_key_indicator(client):
    """ Ensure you cannot delete with foreign key constraints """

    reference_request, reference_response = create_intel_reference(client, 'analyst', 'OSINT', 'http://blahblah.com')
    indicator_request, indicator_response = create_indicator(client, 'IP', '127.0.0.1', 'analyst', TEST_ANALYST_APIKEY, intel_reference='http://blahblah.com', intel_source='OSINT')
    assert reference_request.status_code == 201
    assert indicator_request.status_code == 201

    request = client.delete('/api/intel/reference/{}'.format(reference_response['id']))
    response = json.loads(request.data.decode())
    assert request.status_code == 409
    assert response['message'] == 'Unable to delete intel reference due to foreign key constraints'


def test_delete(client):
    """ Ensure a proper request actually works """

    data = {'value': 'asdf'}
    request = client.post('/api/intel/source', data=data)
    assert request.status_code == 201

    data = {'username': 'analyst', 'reference': 'asdf', 'source': 'asdf'}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    _id = response['id']
    assert request.status_code == 201

    request = client.delete('/api/intel/reference/{}'.format(_id))
    assert request.status_code == 204

    request = client.get('/api/intel/reference/{}'.format(_id))
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['message'] == 'Intel reference ID not found'
