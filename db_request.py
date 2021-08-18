import requests
import json

def url_join(*args):
    res = '/'.join(s.strip('/') for s in args)
    return res

def login_process(credentials):
    s = requests.Session()
    text = url_join(url_address, 'login.json')
    s.post(text, json={'session': credentials})
    print('login into'+text+'successful')
    return s

def get_object_from_id(wear_test_id):
    text = url_join(url_address, 'wear_tests', str(wear_test_id)+'.json?include_associations=true')
    r = requests.get(text)
    my_object = json.loads(json.loads(r.text)['object'])
    return my_object

def check_test_id_exist(wear_test_id):
    text = url_join(url_address, 'wear_tests', str(wear_test_id)+'.json')
    r = requests.get(text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False
    else:
        print('unknown status code.')


def check_scan_exists(filename):
    text = url_join(url_address, 'profilometer_scans', 'find_by_zip_name.json?zip_name='+filename)
    r = requests.get(text)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False
    else:
        print('unknown status code.')

url_address = 'http://131.246.251.61:3000'

if __name__ == '__main__':
    # my_object = get_object_from_id(552428)
    # test = check_test_id_exist(552428)
    test = check_scan_exists('00552428.0000.post.ccl.zip')

    print('finished')