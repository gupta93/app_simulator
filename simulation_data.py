import psycopg2


conn = psycopg2.connect("host=localhost user=odyssey password=odyssey1234 dbname=odyssey_v2")

cur = conn.cursor()

def getAgentInfo():

    #### login data fetch
    try:
        cur.execute('select m.id,m.email,ma.region_id,ma.department_id from member_basic_info m,member_access_rights ma where m.id = ma.member_id and m.id <> m.reporting_manager_id limit 5')
        #cur.execute('select department_id,region_id from member_access_rights')
        return cur
    except Exception,e:
          print str(e)


def getActivityInfo():

    try:
        # cur.execute('select m.id,m.email,m.password_hash,ma.region_id,ma.department_id from member_basic_info m,member_access_rights ma where m.id = ma.member_id and m.id <> m.reporting_manager_id limit 5')
        cur.execute('select id,activity_name from task_activity_type where id <> {}'.format('2909b278-2e62-4594-a230-8f3eabd99ac5'))
        return cur
    except Exception, e:
        print str(e)

