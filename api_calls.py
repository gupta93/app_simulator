import requests, json, datetime
from requests.adapters import HTTPAdapter
from config import NO_OF_SIMULATORS

baseUrl = 'http://139.59.46.228:8001/api/v2/'
requests.Session().mount('http://139.59.46.228', HTTPAdapter(max_retries=10))


def login(email):
    f = open('login_api_response.txt', 'w')

    try:
        print email
        params = {"login_id": email, "password": "loktra","source":"agent_app"}
        start = datetime.datetime.now()
        response = requests.post(url=baseUrl + 'auth/login', data=params)
        end = datetime.datetime.now()
        diff = end - start
        print 'Login ' + str(response.status_code)
        print response.cookies
        f.write('{},{},{},{}'.format(str(NO_OF_SIMULATORS),
                                            str(start.hour) + ':' + str(start.minute) + ':' + str(start.second),
                                            str(diff.total_seconds() * 1000), str(response.status_code)))
        f.write('\n')
        return response.cookies

    except Exception,e:
            f.write(str(e))
            f.write('\n')

def get_home_data(counter, c):
    try:

        start = datetime.datetime.now()
        response = requests.get(baseUrl + 'agent-app/home', cookies=c)
        end = datetime.datetime.now()
        diff = end - start
        home_csv = open('home_api_response.txt', 'a')

        home_csv.write('{},{},{},{}'.format(str(NO_OF_SIMULATORS),str(counter),
                                            str(diff.total_seconds() * 1000), str(response.status_code)))
        home_csv.write('\n')
        print 'Home ' + str(response.status_code)
        if response.status_code != 200:
            return None
        return response.json()
    except:
        return None


def bulk_update(counter, data, cookie,id):

    try:
        to_delete = None
        if len(data['task_details']) > 0:
            for d in data['task_details']:

                if len(d['attempt_details'][0]['activity_details']) <= 2:
                    to_delete = d
                    break
            if to_delete is not None:
                data['task_details'].remove(d)
            f = open('bulk_request.txt', 'a')
            f.write('APPENDING BULK REQUEST \n \n')
            f.write('=================START==============')
            f.write('\n')
            f.write(json.dumps(data))
            f.write('\n')
            f.write('=================END==============')
            f.write('\n')
            f.close()






    except Exception,e:
            f = open('error.log','w')
            f.write('\n \n '+str(e))
            pass
    start = datetime.datetime.now()
    response = requests.post(url=baseUrl + 'agent-app/bulk-update', json=data, cookies=cookie)
    end = datetime.datetime.now()

    data_verified = None
    if response.status_code == 500:
        from functions import verify_data

        # try:
        #     from functions import verify_tasks
        #     data = verify_tasks(data)
        # except:
        #     pass
        try:
            data_verified = verify_data(data,id,open('previous-{}.json'.format(id),'r').read())
        except:
            data_verified = verify_data(data,id,None)
        if not data_verified:
            data = data_verified
            start = datetime.datetime.now()
            response = requests.post(url=baseUrl + 'agent-app/bulk-update', json=data, cookies=cookie)
            end = datetime.datetime.now()

    print 'Update ' + str(response.status_code)

    prev = open('previous-{}.json'.format(id), 'w')
    prev.write(json.dumps(data))
    diff = end - start
    bulk_csv = open('bulk_api_response.txt', 'a')

    bulk_csv.write('{},{},{},{}'.format(str(NO_OF_SIMULATORS), counter,
                                        str(diff.total_seconds() * 1000), str(response.status_code)))
    bulk_csv.write('\n')
    return response.status_code


def locations(data, cookie,counter):
    start = datetime.datetime.now()

    try:
        response = requests.post(url=baseUrl + 'agent-app/locations/update', json=data, cookies=cookie)
        print 'Locations ' + str(response.status_code)
        end = datetime.datetime.now()

        diff = end - start
        location_csv = open('location_api_response.txt', 'a')

        location_csv.write('{},{},{},{}'.format(str(NO_OF_SIMULATORS), counter,
                                                str(diff.total_seconds() * 1000), str(response.status_code)))
        location_csv.write('\n')

    except Exception, e:

        print 'connection refused ' + str(e)


def agentLoginDetails(n,m):
    response = requests.get(url=baseUrl + 'populate_db/get-login-data?agent_count={}&offset={}'.format(str(n),m))
    return response.json()


def get_customer_data():
    response = requests.get(url=baseUrl + 'populate_db/get-customer-data')
    return response.json()


def upload_image(image,id,c,t):

    try:
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{}\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"task_activity_id\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(image,id)
        headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
            }

        response = requests.post(url=baseUrl+'agent-app/image/{}'.format(t),data=payload, headers=headers, cookies=c)


        print 'Image ',response.status_code
    except Exception,e:
        print str(e)
