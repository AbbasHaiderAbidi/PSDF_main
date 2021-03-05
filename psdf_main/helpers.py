from .helper_imports import *


def useronline(request):
    if (request.session.has_key('user')):
        return True
    else:
        return False

def adminonline(request):
    if (request.session.has_key('user') and request.session.has_key('admin')):
        return True
    else:
        return False


def oops(request):
    return render(request, 'psdf_main/404.html')

def userDetails(username):
    user = {}
    userobj = users.objects.filter(username = username)[:1]
    for user1 in userobj:
        user['id'] = user1.id
        user['username'] = user1.username
        user['nodal'] = user1.nodal
        user['contact'] = user1.contact
        user['address'] = user1.address
        user['utilname'] = user1.utilname
        user['region'] = user1.region
        user['lastlogin'] = user1.lastlogin
        user['reqdate'] = user1.reqdate
        user['aprdate'] = user1.aprdate
        user['admin'] = user1.admin
        user['active'] = user1.active
        if user1.notification:
            user['notifications'] = user1.notification.split(']*[')[1:]
        else:
            user['notifications'] = ""
        user['activate'] = user1.activate
    return user

def projectDetails(projid):
    proj = {}
    proj1 = projects.objects.get(id = projid)
    if proj1:
        proj['id'] = proj1.id
        proj['name'] = proj1.name
        proj['dprsubdate'] = proj1.dprsubdate
        proj['amt_asked'] = proj1.amt_asked
        proj['amt_released'] = proj1.amt_released
        proj['schedule'] = proj1.schedule
        proj['fundcategory'] = proj1.fundcategory
        proj['quantum'] = proj1.quantumOfFunding
        proj['extension'] = proj1.extension
        proj['status'] = proj1.status
        proj['remark'] = proj1.remark
        proj['submitted_boq'] = proj1.submitted_boq
        proj['approved_boq'] = proj1.approved_boq
        proj['user_username'] = proj1.userid.username
        proj['user_nodal'] = proj1.userid.nodal
        proj['user_region'] = proj1.userid.region
        proj['user_utilname'] = proj1.userid.utilname
        proj['user_contact'] = proj1.userid.contact
        proj['user_address'] = proj1.userid.address
        proj['user_reqdate'] = proj1.userid.reqdate
        proj['user_aprdate'] = proj1.userid.reqdate
        proj['user_lastlogin'] = proj1.userid.lastlogin
        proj['user_active'] = proj1.userid.active
        return proj
    else:
        return False

def temp_projectDetails(projid):
    proj = {}
    proj1 = temp_projects.objects.get(id = projid)
    if proj1:
        proj['id'] = proj1.id
        proj['name'] = proj1.proname
        proj['dprsubdate'] = proj1.dprsubdate
        proj['amt_asked'] = proj1.amountasked
        proj['deny'] = proj1.deny
        proj['schedule'] = proj1.schedule
        proj['remark'] = proj1.remark
        proj['removed'] = proj1.removed
        eachboq = proj1.submitted_boq[2:-2].split('}, {')
        
        abc = []
        for boq in eachboq :
            attrlist = boq.split(', ')
            
            one_boq={}
            for attr in attrlist:
                attrname = attr.split(':')[0][1:-1]
                attrvalue = attr.split(':')[1][2:-1]
                one_boq[attrname] = attrvalue
            abc.append(one_boq)
        item_Gtotal = {}
        Gtotal_list = []
        for boq in abc:
            if boq['itemname'] in item_Gtotal.keys():
                item_Gtotal[boq['itemname']] = item_Gtotal[boq['itemname']] + boq['itemcost']
            else:
                 item_Gtotal[boq['itemname']] = boq['itemcost']
        for key, value in item_Gtotal.items():
            Gtotal_list.append({'itemname':key, 'grandtotal':value})
        
        proj['submitted_boq_Gtotal'] = Gtotal_list
        proj['submitted_boq_list'] = abc
        proj['user_username'] = proj1.userid.username
        proj['user_nodal'] = proj1.userid.nodal
        proj['user_region'] = proj1.userid.region
        proj['user_utilname'] = proj1.userid.utilname
        proj['user_contact'] = proj1.userid.contact
        proj['user_address'] = proj1.userid.address
        proj['user_reqdate'] = proj1.userid.reqdate
        proj['user_aprdate'] = proj1.userid.reqdate
        proj['user_lastlogin'] = proj1.userid.lastlogin
        proj['user_active'] = proj1.userid.active
        return proj
    else:
        return False

def pen_users(request):
    if adminonline(request):
        penuser = users.objects.filter(activate = False)
        if penuser:
            return penuser
        else:
            return False
    else:
        return False

def pen_users_num(request):
    if adminonline(request):
        penuser = pen_users(request)
        if penuser:
            penuser.count()
        else:
            return False
    else:
        return False


def get_all_users(request):
    if adminonline(request):
        usersobj = users.objects.filter(admin = False)
        allusers = []
        for userobj in usersobj:
            allusers.append(userDetails(userobj.username))
        return allusers
    else:
        return False


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def isnum(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def smkdir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True
    except:
        return False


def srmdir(filename):
    try:
        shutil.rmtree(filename, ignore_errors=True)
        return True
    except OSError:
        return False

def handle_uploaded_file(path, f):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()



def getTempProjects(request):
    if adminonline(request):
        temp_project_list = []
        temp_project = temp_projects.objects.all().exclude(deny = True)
        for proj in temp_project:
            temp_project_list.append(temp_projectDetails(proj.id))
        return temp_project_list
    return False

