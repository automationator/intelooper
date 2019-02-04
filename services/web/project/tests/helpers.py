import json


def create_auth_header(token):
    return {'Authorization': 'Bearer {}'.format(token)}


def obtain_token(client, username, password):
    request = client.post('/auth', data={'username': username, 'password': password})
    response = json.loads(request.data.decode())
    return response['access_token'], response['refresh_token']


def create_campaign(client, campaign, aliases=[]):
    data = {'name': campaign, 'aliases': aliases}
    request = client.post('/api/campaigns', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_campaign_alias(client, alias, campaign):
    data = {'alias': alias, 'campaign': campaign}
    request = client.post('/api/campaigns/alias', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event(client, name, username, attack_vector='', campaign='', disposition='', malware='', prevention_tool='',
                 remediation='', status='', tags='', types='', intel_reference='', intel_source=''):
    if not disposition:
        disposition = 'asdf'
    create_event_disposition(client, disposition)

    if not status:
        status = 'asdf'
    create_event_status(client, status)

    data = {'name': name, 'username': username, 'disposition': disposition, 'status': status}
    if attack_vector:
        create_event_attack_vector(client, attack_vector)
        data['attack_vectors'] = attack_vector
    if campaign:
        create_campaign(client, campaign)
        data['campaign'] = campaign
    if malware:
        malware = malware.split(',')
        for m in malware:
            create_malware(client, m)
        data['malware'] = malware
    if prevention_tool:
        create_event_prevention_tool(client, prevention_tool)
        data['prevention_tools'] = prevention_tool
    if remediation:
        create_event_remediation(client, remediation)
        data['remediations'] = remediation
    if tags:
        tags = tags.split(',')
        for tag in tags:
            create_tag(client, tag)
        data['tags'] = tags
    if types:
        types = types.split(',')
        for _type in types:
            create_event_type(client, _type)
        data['types'] = types
    if intel_reference and intel_source:
        create_intel_reference(client, username, intel_source, intel_reference)
        data['references'] = intel_reference

    request = client.post('/api/events', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_attack_vector(client, attack_vector):
    data = {'value': attack_vector}
    request = client.post('/api/events/attackvector', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_disposition(client, disposition):
    data = {'value': disposition}
    request = client.post('/api/events/disposition', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_prevention_tool(client, prevention_tool):
    data = {'value': prevention_tool}
    request = client.post('/api/events/preventiontool', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_remediation(client, remediation):
    data = {'value': remediation}
    request = client.post('/api/events/remediation', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_status(client, status):
    data = {'value': status}
    request = client.post('/api/events/status', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_event_type(client, _type):
    data = {'value': _type}
    request = client.post('/api/events/type', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_indicator(client, _type, value, username, campaigns='', case_sensitive=False, confidence='', impact='',
                     intel_reference='', intel_source='', status='', substring=False, tags=''):
    create_indicator_type(client, _type)

    if not confidence:
        confidence = 'LOW'
    create_indicator_confidence(client, confidence)

    if not impact:
        impact = 'LOW'
    create_indicator_impact(client, impact)

    if not status:
        status = 'New'
    create_indicator_status(client, status)

    data = {'case_sensitive': case_sensitive, 'confidence': confidence, 'impact': impact, 'status': status,
            'substring': substring, 'type': _type, 'username': username, 'value': value}
    if campaigns:
        campaigns = campaigns.split(',')
        for campaign in campaigns:
            create_campaign(client, campaign)
        data['campaigns'] = campaigns
    if tags:
        tags = tags.split(',')
        for tag in tags:
            create_tag(client, tag)
        data['tags'] = tags
    if intel_reference and intel_source:
        create_intel_reference(client, username, intel_source, intel_reference)
        data['references'] = intel_reference

    request = client.post('/api/indicators', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_indicator_confidence(client, confidence):
    data = {'value': confidence}
    request = client.post('/api/indicators/confidence', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_indicator_impact(client, impact):
    data = {'value': impact}
    request = client.post('/api/indicators/impact', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_indicator_status(client, status):
    data = {'value': status}
    request = client.post('/api/indicators/status', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_indicator_type(client, _type):
    data = {'value': _type}
    request = client.post('/api/indicators/type', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_intel_reference(client, username, source, reference):
    create_intel_source(client, source)

    data = {'username': username, 'reference': reference, 'source': source}
    request = client.post('/api/intel/reference', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_intel_source(client, source):
    data = {'value': source}
    request = client.post('/api/intel/source', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_malware(client, malware, types=[]):
    data = {'name': malware, 'types': types}
    request = client.post('/api/malware', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_malware_type(client, _type):
    data = {'value': _type}
    request = client.post('/api/malware/type', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_role(client, role):
    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'name': role}
    request = client.post('/api/roles', data=data, headers=headers)
    response = json.loads(request.data.decode())
    return request, response


def create_tag(client, tag):
    data = {'value': tag}
    request = client.post('/api/tags', data=data)
    response = json.loads(request.data.decode())
    return request, response


def create_user(client, email, first_name, last_name, password, roles, username):
    access_token, refresh_token = obtain_token(client, 'admin', 'admin')
    headers = create_auth_header(access_token)

    data = {'email': email, 'first_name': first_name, 'last_name': last_name,
            'password': password, 'roles': roles, 'username': username}
    request = client.post('/api/users', data=data, headers=headers)
    response = json.loads(request.data.decode())
    return request, response
