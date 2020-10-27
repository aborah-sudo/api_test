import requests


def get_token():
    url = 'https://api.discovery-staging.verifiable.com/auth/token/password'
    headers = {'content-type': 'application/json'}
    data = {"email": "mail@gmail.com", "password": "sasa"}
    req = requests.post(url, headers=headers, json=data)
    return req.text


def test_licence_found():
    pre_token = get_token()
    token_id = pre_token.split('"')[3]
    token = pre_token.split('"')[7]
    found = "https://api.discovery-staging.verifiable.com/providers/{providerId}/licenses/{id}"
    hed = {'Authorization': 'Bearer ' + token}
    result = requests.get(found, headers=hed).json()
    print("Found")
    assert result["licenseNumber"] == "8"


def test_licence_not_found():
    pre_token = get_token()
    token_id = pre_token.split('"')[3]
    token = pre_token.split('"')[7]
    not_found = "https://api.discovery-staging.verifiable.com/providers/{providerId}/licenses/{id}"
    hed = {'Authorization': 'Bearer ' + token}
    result = requests.get(not_found, headers=hed).json()
    print("Not Found")
    assert result['status'] == 404


def test_multi_status():
    pre_token = get_token()
    token_id = pre_token.split('"')[3]
    token = pre_token.split('"')[7]
    url = "https://api.discovery-staging.verifiable.com/providers/{providerId}/licenses"
    hed = {'Authorization': 'Bearer ' + token}
    result = requests.get(url, headers=hed).json()
    status_found = [data for data in result if data['currentVerificationStatus'] == 'Found']
    status_not_found = [data for data in result if data['currentVerificationStatus'] == 'NotFound']
    status_needs_review = [data for data in result if data['currentVerificationStatus'] == 'NeedsReview']
    print(f'{len(status_found)} in Found status')
    print(f'{len(status_not_found)} in Not Found status')
    print(f'{len(status_needs_review)} in NeedsReview status')
