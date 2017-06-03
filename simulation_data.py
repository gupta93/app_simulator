import sys, datetime, time

from api_calls import login, get_home_data, bulk_update, get_customer_data, agentLoginDetails
from functions import *
from random import randint
from config import *
from threading import Thread
import threading


class Location(Thread):
    def __init__(self, agent):
        Thread.__init__(self)
        self.agent_data = agent
        self.time_interval = INTERVAL_LOCATION_ACTIVITY
        self.max_size = 60
        self.stop = False
        self.counter = 0

    def run(self):
        while not self.stop:
            st = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - st).total_seconds() >= self.time_interval:
                    break

            self.counter+=1
            points_file = open('points.json', 'r')
            point_data = json.loads(points_file.read())['data']
            form_location_data(self.agent_data, point_data,self.counter)


class BulkUpdate(Thread):
    def __init__(self, agent):
        Thread.__init__(self)
        self.agent_data = agent
        self.time_interval = INTERVAL_BULK_UPDATE
        self.stop = False
        self.counter = 0

    def run(self):

        while not self.stop:
            st = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - st).total_seconds() >= self.time_interval:
                    break

            try:
                bulk_file = open('bulk-{}.json'.format(self.agent_data['id']), 'r')
                update_data = bulk_file.read()
                self.counter += 1
                resp = bulk_update(str(self.counter), json.loads(update_data), self.agent_data['cookie'],self.agent_data['id'])
                bulk_file.close()

                bulk = open('bulk-{}.json'.format(self.agent_data['id']), 'w')
                bulk.write(json.dumps({}))
                bulk.close()
            except:
                pass
class ImageUpdate(Thread):
    def __init__(self,agent):
        Thread.__init__(self)
        self.agent_data = agent
        self.time_interval = INTERVAL_IMAGE_ACTIVITY
        self.startt = False
        self.stop = False
        self.done = []

    def run(self):

        while not self.stop:
            if not self.startt:
                st = datetime.datetime.now()
                while True:
                    if (datetime.datetime.now() - st).total_seconds() >= INTERVAL_BULK_UPDATE+60:
                        self.startt = True
                        break



            try:
                print 'image run function'+self.agent_data['id']
                data = open('agent-{}.json'.format(self.agent_data['id']),'r')

                dataa = json.loads(data.read())
                from functions import add_image
                self.done = add_image(dataa,self.agent_data['cookie'],self.done)
            except:
                print 'errorrr image'
                pass
            st = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - st).total_seconds() >= self.time_interval:
                    break


class Tasks(Thread):
    def __init__(self, agent):
        Thread.__init__(self)
        self.agent_data = agent
        self.time_interval = INTERVAL_CREATE_TASKS
        self.stop = False


    def run(self):

        while not self.stop:
            st = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - st).total_seconds() >= self.time_interval:
                    break




            try:
                file_read = open('agent-{}.json'.format(self.agent_data['id']), 'r')
                data = json.loads(file_read.read())
                file_read.close()
                if data is None:
                    pass
            except:
                pass
            customer_data = get_customer_data()
            try:
                customer_id = customer_data['message']['id']
                customer_address_id = customer_data['message']['address_id']
            except:
                customer_address_id = 'bafdcd33-8ef2-4b01-97c6-d23a957923fb'
                customer_id = '93c8ae00-bb90-4a9c-b001-70d7e1f09eb1'
            manager = self.agent_data['manager_id']
            region = self.agent_data['region_id']
            department = self.agent_data['department_id']

            task_data = create_task(self.agent_data['id'], customer_id, customer_address_id, manager, region, department)
            try:
                old_data = data['task_details']
                old_data.append(task_data)
                data['task_details'] = old_data
            except:
                data = {}
                data['task_details'] = []
                data['task_details'].append(task_data)
            print 'writing new task \n {}'.format(task_data['id'])
            print '\n agent is {}'.format(task_data['active_agent_id'])
            file_write = open('agent-{}.json'.format(self.agent_data['id']), 'w')
            file_write.write(json.dumps(data))
            file_write.close()





class Agent(Thread):
    def __init__(self, a):
        Thread.__init__(self)

        self.agent_id = a['id']

        self.region_id = a['region_id']
        self.department_id = a['department_id']
        self.manager_id = a['manager_id']
        self.task_complete_step = '4'
        self.self_assign = '5'
        self.api_cookie = None
        self.bulk_counter = 0
        self.home_counter = 0
        self.location_counter = 0
        self.current_task_index = 0
        self.current_activity_status = ''
        self.bulk_data = None
        self.task_complete = []
        self.status = False
        self.is_on = False
        self.shift_timestamp = str(datetime_object_to_string(datetime.datetime.now()))

        self.interval = INTERVAL_TASK_ACTIVITY
        self.previous_task_index = -1
    def run(self):
        self.login_simulator()
        #self.home_simulator(1)

    def login_simulator(self):
        self.api_cookie = login(self.agent_id)

    def shift_on(self):

        last = open('bulk-{}.json'.format(self.agent_id), 'r')
        data = json.loads(last.read())
        last.close()
        data['activity_details'] = []
        data['activity_details'].append({
            'id': str(uuid.uuid4()),
            'activity_type': '02c577b2-5a8b-4064-9a38-896677e05c39',
            'actual_timestamp': self.shift_timestamp,
            'agent_location': {},
            'remarks': ''

        })

        final_write = open('bulk-{}.json'.format(self.agent_id), 'w')
        final_write.write(json.dumps(data))
        final_write.close()
        self.is_on = True

    # def home_simulator(self,flag):
    #
    #     if flag==1:
    #         self.home_counter+=1
    #         home_data = get_home_data(str(self.home_counter), self.api_cookie)
    #     else:
    #         f11 = open('agent-{}.json'.format(self.agent_id),'r')
    #         home_data = json.loads(f11.read())
    #     if home_data is None:
    #         pass
    #     else:
    #         try:
    #             f = open('agent-{}.json'.format(self.agent_id), 'w')
    #             f.write(json.dumps(home_data))
    #             f.close()
    #
    #             if len(home_data['task_details']) > 0:
    #                 try:
    #                     self.agent_id = home_data['task_details'][0]['active_agent_id']
    #                 except:
    #                     pass
    #                 try:
    #                     self.region_id = home_data['task_details'][0]['region_id']
    #                 except:
    #                     pass
    #                 try:
    #                     self.department_id = home_data['task_details'][0]['department_id']
    #                 except:
    #                     pass
    #                 try:
    #                     self.manager_id = home_data['task_details'][0]['attempts'][0]['last_activity']['manager_id']
    #                 except:
    #                     pass
    #                 print 'agent is {}'.format(self.agent_id)
    #                 print 'completed {}'.format(str(len(self.task_complete)))
    #                 print 'total {}'.format(str(len(home_data['task_details'])))
    #                 if len(self.task_complete) == len(home_data['task_details']):
    #
    #                     # bulk_update(self.agent_id,self.bulk_data,self.api_cookie)
    #                     self.status = True
    #                 else:
    #                     # print len(self.task_complete)
    #                     # print len(home_data['task_details'])
    #                     self.current_task_index = len(self.task_complete)
    #                     self.current_task_id = home_data['task_details'][self.current_task_index]['id']
    #                     try:
    #                         self.current_activity_status = home_data['task_details'][self.current_task_index][
    #                             'current_activity_status']
    #                     except:
    #                         self.current_activity_status = 'ASSIGN AGENT'
    #
    #         except:
    #             return

    def task_simulator(self):

        while True:
            print 'Current Task Index '+str(self.current_task_index)

            try:
                if self.current_task_index == self.previous_task_index:
                    tasks_read = open('bulk-{}.json'.format(self.agent_id), 'r')
                else:
                    tasks_read = open('agent-{}.json'.format(self.agent_id), 'r')
                    self.previous_task_index = self.current_task_index


                home_data = json.loads(tasks_read.read())
                tasks_read.close()

                if 'task_details' in home_data and len(home_data['task_details'])>=self.current_task_index+1:
                    self.current_activity_status = home_data['task_details'][self.current_task_index]['current_actitvity_status']

                    status = ''
                    activity_id = ''

                    if self.current_activity_status == 'CREATED':
                        status = 'ASSIGN AGENT'
                        activity_id = '2f514e90-9079-4024-81f6-fe16061ad859'
                    elif self.current_activity_status == 'ASSIGN AGENT' or self.current_activity_status == 'ACKNOWLEDGED':
                        status = 'STARTED'
                        activity_id = '1e120260-147a-4453-b1fb-2199345a6d06'

                    elif self.current_activity_status == 'STARTED':
                        status = 'AGENT ARRIVED'
                        activity_id = '98b19f55-e5c2-4972-8a3a-e977ecf4d167'
                    elif self.current_activity_status == 'AGENT ARRIVED' or self.current_activity_status == 'MEETING STARTED':
                        status = 'SUCCESS'
                        activity_id = '7153ea57-8241-4e0d-b992-3f3c677df5c2'
                    elif self.current_activity_status == 'SUCCESS':
                        img = True
                        i = randint(0, 1)
                        if i == 0:
                            status = 'REVISIT'
                            activity_id = '4c749952-2817-464a-b288-f52668e35805'
                        else:
                            status = 'Done'
                            activity_id = ''

                    elif self.current_activity_status == 'FAILED':
                        img = True
                        i = randint(0, 1)
                        if i == 0:
                            status = 'REVISIT'
                            activity_id = '4c749952-2817-464a-b288-f52668e35805'
                        else:
                            status = 'Done'
                            activity_id = ''

                    print self.current_activity_status
                    self.current_activity_status = status

                    self.current_task_id = home_data['task_details'][self.current_task_index]['id']
                    if self.bulk_data is None:

                        data = home_data['task_details'][self.current_task_index]
                        result = {}
                        result['task_details'] = []
                        result['task_details'].append(home_data['task_details'][self.current_task_index])

                        result = edit_task_function(agent_id=self.agent_id, result=result, flag=1, activity=activity_id,
                                                    status=self.current_activity_status, data=data,
                                                    task_id=self.current_task_id)
                        self.bulk_data = result
                    else:

                        if status != 'Done' and activity_id != '':

                            if 'task_details' not in self.bulk_data:
                                self.bulk_data['task_details'] = []
                                self.bulk_data['task_details'].append(home_data['task_details'][self.current_task_index])

                            data = home_data['task_details'][self.current_task_index]
                            self.bulk_data = edit_task_function(agent_id=self.agent_id, result=self.bulk_data, flag=1,
                                                                activity=activity_id,
                                                                status=self.current_activity_status,
                                                                data=data, task_id=self.current_task_id)

                        else:

                            print 'calling for new task \n'
                            self.previous_task_index = self.current_task_index
                            self.current_task_index += 1

                    bulk_write = open('bulk-{}.json'.format(self.agent_id), 'w')
                    bulk_write.write(json.dumps(self.bulk_data))
                    bulk_write.close()
                    if not self.is_on:
                        self.shift_on()

            except Exception,e:
                print 'Simulator Exception \n '+str(e)
                pass



            startt = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - startt).total_seconds() >= self.interval:
                    break


def start_location(agentss):
    loc = Location(agentss)
    loc.start()

    return loc


def start_create_tasks(agentss):
    task = Tasks(agentss)
    task.start()
    return task


def update(agentss):
    updates = BulkUpdate(agentss)
    updates.start()
    return updates

def images(agentss):
    image = ImageUpdate(agentss)
    image.start()
    return image

def simulate(agent):

     agent_ids = {}
     print agent
     a = Agent(agent)
     a.start()
     a.join()

     agent_data = {'id': a.agent_id,
                          'cookie': a.api_cookie, 'region_id': a.region_id,
                          'department_id': a.department_id, 'manager_id': a.manager_id,'bulk':a.bulk_counter,'loc':a.location_counter,'home':a.home_counter}

     if LOCATIONS:
        loc = start_location(agent_data)
     if TASKS:
        task = start_create_tasks(agent_data)
     if BULK_UPDATE:
        bulk = update(agent_data)
     if IMAGE:
        img = images(agent_data)

 #    a.home_simulator()
    # a.join()
     start = datetime.datetime.now()

     a.task_simulator()
