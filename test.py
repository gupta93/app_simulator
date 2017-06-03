
from odyssey.v2.precomputations.functions import precompute_agent_location_snapshot
from odyssey.v2.precomputations.functions import precompute_dr
from odyssey.v2.precomputations.functions import precompute_drm
from odyssey.v2.precomputations.functions import precompute_member_data
from odyssey.v2.precomputations.functions import precompute_manager_reportee_tree_mapping
from odyssey.v2.precomputations.functions import precompute_mis_member_data
from odyssey.v2.common.utils import send_users
from odyssey.v2.groups.precomputations import create_department_mapping
from odyssey.v2.groups.precomputations import create_region_mapping
from odyssey.v2.precomputations.functions import precompute_day_wise_last_location
from odyssey.v2.periodic_mails.functions import send_inactive_members_email
from odyssey.v2.precomputations.functions import precompute_admin_member_access
import datetime

f = open('time_log_precompute.log','a')
f1 = open('error.log','a')
def master_function():

    try:
        start  = datetime.datetime.now()
        precompute_agent_location_snapshot()
        f.write('\n \n  Agent Location Snapshot : '+str((datetime.datetime.now()-start).total_seconds()))
    except:
        f1.write('\n \nerror in  Agent Location Snapshot')
        pass
    try:
        start  = datetime.datetime.now()
        precompute_drm()
        f.write('\n \n Precompute Drm : '+str((datetime.datetime.now()-start).total_seconds()))

    except:
        f1.write('\n \n error in Precompute Drm')
        pass
    try:
        start  = datetime.datetime.now()
        precompute_dr()
        f.write('\n \n Precompute Dr: '+str((datetime.datetime.now()-start).total_seconds()))

    except:
        f1.write('\n \n error in Precompute Dr')

        pass
    try:
        start  = datetime.datetime.now()
        precompute_member_data()
        f.write('\n \n Precompute Member Data : '+str((datetime.datetime.now()-start).total_seconds()))

    except:
        f1.write('\n \n error in Precompute Membr data')

        pass
    try:
        start  = datetime.datetime.now()
        precompute_manager_reportee_tree_mapping()
        f.write('\n \n Precompute Manager Report : '+str((datetime.datetime.now()-start).total_seconds()))

    except:
        f1.write('\n \n error in Manager report')

        pass
    try:
        start  = datetime.datetime.now()
        precompute_mis_member_data()
        f.write('\n \n Precompute MIS : '+str((datetime.datetime.now()-start).total_seconds()))

    except:
        f1.write('\n \n error in Precompute MIS')

        pass
    try:
        start  = datetime.datetime.now()
        send_users()
        f.write('\n \n Precompute Send Users : '+str((datetime.datetime.now()-start).total_seconds()))

    except:

        f1.write('\n \n error in Precompute send users')

        pass
    try:
        start  = datetime.datetime.now()
        create_department_mapping()
        f.write('\n \n Department Mapping : '+str((datetime.datetime.now()-start).total_seconds()))

    except:

        f1.write('\n \n error in Precompute dept mappng')

        pass
    try:
        start  = datetime.datetime.now()
        create_region_mapping()
        f.write('\n \n Region Mapping : '+str((datetime.datetime.now()-start).total_seconds()))

    except:

        f1.write('\n \n error in Precompute region mappping')

        pass
    try:
        start  = datetime.datetime.now()
        precompute_day_wise_last_location()
        f.write('\n \n Precompute Day Wise Last Location : '+str((datetime.datetime.now()-start).total_seconds()))

    except:

        f1.write('\n \n error in Precompute day wise last loc')

        pass
    try:
        start  = datetime.datetime.now()
        precompute_admin_member_access()
        f.write('\n \n Precompute Admin Member Access : '+str((datetime.datetime.now()-start).total_seconds()))

    except:

        f1.write('\n \n error in Precompute admin member access')
        pass