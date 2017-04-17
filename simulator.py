import sys,requests
import datetime
from simulation_data import getAgentInfo
from api_calls import login, get_home_data, bulk_update
from multiprocessing.pool import ThreadPool,Process,Queue
from multiprocessing import cpu_count
from functions import *
from random import randint


import threading
from threading import Thread

thread_array = []


class Agent(Thread):
    def __init__(self,a):

        Thread.__init__(self)
        self.agent_id = a[0]
        self.password = a[1]
        self.email = a[2]
        self.region_id = a[3]
        self.department_id = a[4]
        self.lock = threading.Lock()

    def run(self):
        self.login_simulator()

    def login_simulator(self):
        if login(self.email):
            self.home_simulator()
            self.task_simulator()

    def home_simulator(self):
        home_data = get_home_data(self.agent_id)
        f = open('agent-{}.json'.format(self.agent_id),'w')
        f.write(home_data)

    def logout(self):
        pass
    def task_simulator(self):



          f = open('agent-{}.json'.format(self.agent_id), 'r')
          data = json.loads(f.read())

          home_data = data['task_details']
          result = {}
          result['task_details'] = []
          ind = 0
          for data in home_data:

             result =  edit_task_function(self.agent_id,result,ind,data,randint(0,1))
             ind+=1

          bulk_update(self.agent_id,result)
          self.home_simulator()
          self.logout()







def execute(agents):

        for ag in agents:
               a = Agent(ag)
               thread_array.append(a)


        for thread in thread_array:
            thread.start()
            print 'thread waiting for commands. {}'.format(thread.agent_id)








if __name__ == "__main__":

        agents = getAgentInfo()

        # for r in regions:
        #
        #         p = Process(target=execute, args=(r,))
        #         p.start()
        for ag in agents:
               a = Agent(ag)
               thread_array.append(a)


        for thread in thread_array:
            thread.start()
            print 'thread waiting for commands. {}'.format(thread.agent_id)






