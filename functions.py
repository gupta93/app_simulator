from random import randint
import json, uuid, datetime, math


def edit_task_function(agent_id, result, flag, activity=None, status=None, data=None, task_id=None):
    try:
        if flag == 0:

           pass
        elif flag == 1:

            print 'inside add activity'
            found = False

            ind = 0

            for task in result['task_details']:


                if task['id'] == task_id:
                    found = True
                    data = task
                    break
                ind += 1

            if not found:
                ind = len(result['task_details'])
                result['task_details'].append({})

            # else:
            #     ind = len(result['task_details'])
            #     result['task_details'].append({})



            result['task_details'][ind]['id'] = task_id
            result['task_details'][ind]['current_activity_status'] = status
            result['task_details'][ind]['last_updated_on'] = datetime_object_to_string(datetime.datetime.now())
            try:
                result['task_details'][ind]['current_attempt_number'] = data['attempts'][-1]['current_attempt_number']
            except:
                result['task_details'][ind]['current_attempt_number'] = 1

            activity_id = str(uuid.uuid4())

            if 'attempt_details' not in result['task_details'][ind]:

                result['task_details'][ind]['current_agent_id'] = agent_id
                if status == 'REVISIT':
                    try:
                        result['task_details'][ind]['current_attempt_number'] +=1
                    except:
                        result['task_details'][ind]['current_attempt_number'] = 2

                    activity_data = {

                        'id': str(uuid.uuid4()),
                        'last_activity_timestamp': datetime_object_to_string(datetime.datetime.now()),
                        'revisit_timestamp': datetime_object_to_string(datetime.datetime.now()),
                        'last_activity_id': activity_id,
                        'attempt_number': result['task_details'][ind]['current_attempt_number'],
                        'activity_details': [
                            {
                                'id': activity_id,
                                'agent_id': agent_id,
                                'type_id': activity,
                                'actual_timestamp': datetime_object_to_string(datetime.datetime.now()),
                                'collections':[]
                            }
                        ]

                    }
                    result['task_details'][ind]['attempt_details'] = []

                    result['task_details'][ind]['attempt_details'].append(activity_data)
                else:

                    try:
                        activity_data = {

                            'id': data['attempts'][-1]['attempt_id'],
                            'last_activity_timestamp': data['attempts'][-1]['last_activity_timestamp'],
                            'last_activity_id': activity_id,
                            'attempt_number': 1,
                            'activity_details': [
                                {
                                    'id': activity_id,
                                    'agent_id': agent_id,
                                    'type_id': activity,
                                    'actual_timestamp': datetime_object_to_string(datetime.datetime.now()),
                                    'collections':[]
                                }
                            ]
                        }



                        result['task_details'][ind]['attempt_details'] = []
                        # result['task_details'][ind]['attempt_details'].append([])
                        result['task_details'][ind]['attempt_details'].append(activity_data)
                    except Exception, e:
                        f = open('error.log', 'w')
                        f.write('\n \n {}'.format(str(e)))
                        f.close()

            else:

                if status == 'REVISIT':
                    try:
                        result['task_details'][ind]['current_attempt_number'] += 1
                    except:
                        result['task_details'][ind]['current_attempt_number'] = 2

                    activity_data = {

                        'id': str(uuid.uuid4()),
                        'last_activity_timestamp': datetime_object_to_string(datetime.datetime.now()),
                        'revisit_timestamp': datetime_object_to_string(datetime.datetime.now()),
                        'last_activity_id': activity_id,
                        'attempt_number': result['task_details'][ind]['current_attempt_number'],
                        'activity_details': [
                            {
                                'id': activity_id,
                                'agent_id': agent_id,
                                'type_id': activity,
                                'actual_timestamp': datetime_object_to_string(datetime.datetime.now()),
                                'collections':[]
                            }
                        ]

                    }
                    result['task_details'][ind]['attempt_details'].append(activity_data)


                else:
                    print 'heree \n'
                    # print result['task_details'][ind]['attempt_details']
                    result['task_details'][ind]['attempt_details'][-1]['last_activity_timestamp'] = \
                        result['task_details'][ind]['attempt_details'][-1]['activity_details'][-1]['actual_timestamp']
                    result['task_details'][ind]['attempt_details'][-1]['last_activity_id'] = \
                        activity_id
                    result['task_details'][ind]['attempt_details'][-1]['activity_details'].append(
                        {
                            'id': activity_id,
                            'agent_id': agent_id,
                            'type_id': activity,
                            'actual_timestamp': datetime_object_to_string(datetime.datetime.now()),
                            'collections':[]
                        }
                    )


            return result

    except Exception,e:
        print 'Function exception \n '+ str(e)
        return result

def create_task(agent_id, customer_id, address_id, manager, region, department):
    activity_id = str(uuid.uuid4())
    timestamp =  datetime_object_to_string(datetime.datetime.now())
    data = {

        'id': str(uuid.uuid4()),
        'title': 'Simulator Task',
        'note': 'Simulator Note',
        'active_agent_id': agent_id,
        'active_manager_id': manager,
        'region_id': region,
        'department_id': department,
        'customer_id': customer_id,
        'customer_address_id': address_id,
        'created_on': datetime_object_to_string(datetime.datetime.now()),
        'last_updated_on': datetime_object_to_string(datetime.datetime.now()),
        'current_actitvity_status': 'ASSIGN AGENT',
        'created_by': agent_id,
        "current_task_status": "ACTIVE",
        "customer_address_id": address_id,
        "customer_id": customer_id,
        'current_attempt_number': 1,
        'attempt_details': [

            {
                "id":str(uuid.uuid4()),
                "last_activity_timestamp": timestamp,


                "last_activity_id": activity_id,
                "attempt_number":1,
                "activity_details":[
                    {
                        "id":activity_id,
                        "agent_id":agent_id,
                        "actual_timestamp": timestamp,
                        "type_id":"2f514e90-9079-4024-81f6-fe16061ad859"
                    }
                ]

            }
        ]

    }

    return data


def form_location_data(agents, data,counter):


        start = randint(0, 270)
        agent_location_data = data[start:start + 60]
        json_data = []
        for loc in agent_location_data:
            json_data.append({
                'id': agents['id'],
                'location': {
                    "type": "Point",
                    "coordinates": [loc['lat'], loc['long']]
                },
                'timestamp': str(datetime_object_to_string(datetime.datetime.now()))
            })

        final = {}
        final['user_id']=agents['id']
        final['locations'] = json_data
        from api_calls import locations
        locations(final, agents['cookie'],str(counter))


def datetime_object_to_string(datetime_object):
    if datetime_object is None:
        return None
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime_object.strftime(date_format)




def add_image(data,cookie,res):

    try:

        for i in range(0,len(data['task_details'])):
            print data['task_details'][i]['current_activity_status']
            if data['task_details'][i]['current_activity_status'] == 'SUCCESS' or data['task_details'][i]['current_activity_status'] == 'FAILED':

                activity_id = data['task_details'][i]['attempts'][-1]['last_activity_id']
                print activity_id
                if activity_id not in res:
                    from api_calls import upload_image

                    upload_image('sig.jpg',activity_id,cookie,'signature')


                    upload_image('doc.jpg', activity_id, cookie, 'document')
                    res.append(activity_id)


    except:
        print 'no actvity found'
        pass

    return res
def get_all_activities(data1,data2):

    result = []
    if data1:
        for task in data1['task_details']:
            for attempt in task['attempts']:
                result.append(attempt['last_activity_id'])

    if data2:
        for task in data2['task_details']:
            for attempt in task['attempt_details']:
                for activity in attempt['activity_details']:
                    result.append(activity['id'])

    return result


def verify_data(data,id,prev):

    try:
        try:
            f = open('agent-{}.json'.format(id), 'r')
            home_data = json.loads(f.read())
        except:
            home_data = None
        activity_ids = get_all_activities(home_data,prev)
        for i in range(0,len(data['task_details'])):

            for j in range(0,len(data['task_details'][i]['attempt_details'])):

                for k in range(0,len(data['task_details'][i]['attempt_details'][j]['activity_details'])):


                            activity  = data['task_details'][i]['attempt_details'][j]['activity_details'][k]
                            if activity['id'] in activity_ids:
                                data['task_details'][i]['attempt_details'][j]['activity_details'].remove(activity)


        return data


    except:
        return None
def verify_tasks(data):


    idss =[]
    for task in data['task_details']:

        if task['id'] not in idss:
            idss.append(task['id'])
        else:
            data['task_details'].remove(task)


    return data