from random import randint
import json, uuid
activity_ids = ["f9b17a64-4ce2-4f45-a5da-fc27be06d663", "32c4e935-c5e2-4584-ac5c-6d7f0bfc3099", "8c13e15c-bc7e-4abc-9ce7-decb2f30e97e", "cffd03a0-ecdb-46d1-bfa8-112e25a03b7c"]
def edit_task_function(agent_id,result,ind,data,flag):

    if flag == 0:

        result['task_details'][ind] = {}
        result['task_details'][ind]['id'] = data['id']
        result['task_details'][ind]['title'] = data['title'] + ' edit'

        return result
    elif flag == 1:



       result['task_details'][ind] = {}
       result['task_details'][ind]['id'] = data['id']
       result['task_details'][ind]['current_activity_status'] = data['current_activity_status']
       result['task_details'][ind]['current_attempt_number'] = data['current_attempt_number']


       data = {

           'id':data['attempts'][0]['attempt_id'],
           'last_activity_timestamp':data['attempt'][0]['last_activity_timestamp'],
           'last_activity_id':data['attempt'][0]['last_activity_id'],
           'attempt_number':data['attempt'][0]['attempt_number'],
           'activity_details':[
               {
                   'id':uuid.uuid4(),
                   'agent_id':agent_id,
                   'type_id':activity_ids[randint(0,len(activity_ids)-1)]
               }
           ]
       }

       if 'attempt_details' in result['task_details'][ind]:
           result['task_details'][ind]['attempt_details'].append(data)
       else:
           result['task_details'][ind]['attempt_details'] = []
           result['task_details'][ind]['attempt_details'][0] = {}
           result['task_details'][ind]['attempt_details'][0] = data


       return result
