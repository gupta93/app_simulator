import requests, json

baseUrl = 'https://beta-test.loktra.com/api/v2/'


def login(email):

    params = {"login_id":email,"password":"loktra"}
    response = requests.post(url = baseUrl+'auth/login',data = json.dumps(params))
    response = response.json()
    if response['message'] == "success":
        return True
    else:
        return False

def get_home_data(agent_id):

    try:
        response = requests.get(baseUrl+'agent-app/home/{}'.format(agent_id))
        return response.json()
    except:
        return None

def bulk_update(agent_id,data):

    params = {"activity":data }
    response = requests.post(url=baseUrl + 'agents-app/{}/bulk-update', data=json.dumps(params))
    print response.status_code
