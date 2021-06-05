from .helpers import *



def control_panel(request):
    if adminonline(request):
        user = userDetails(request.session['user'])
        nopendingusers = pen_users_num(request)
        if not nopendingusers:
            nopendingusers = 0
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_control_panel.html', context)
    else:
        return oops(request)
    
    
def uploadformat(request):
    filelist = {'support':'DPR_Supporting_documents.zip', 'format':'DPR_Forms.zip','sample1':'sample1.zip','sample2':'sample2.zip','sample3':'sample3.zip'}
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassF' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return control_panel(request)
            adminpassF = req['adminpassF']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return control_panel(request)
            if request.FILES:
                files = request.FILES
                if 'support' in files.keys():
                    naam = 'support'
                    formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/Formats/')
                    handle_uploaded_file(os.path.join(formatpath,filelist[naam]),files[naam])
                    messages.success(request, 'Supporting Documents updated.')
                if 'format' in files.keys():
                    naam = 'format'
                    formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/Formats/')
                    handle_uploaded_file(os.path.join(formatpath,filelist[naam]),files[naam])
                    messages.success(request, 'Format updated.')
                if 'sample1' in files.keys():
                    naam = 'sample1'
                    formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/Formats/')
                    handle_uploaded_file(os.path.join(formatpath,filelist[naam]),files[naam])
                    messages.success(request, 'Sample 1 updated.')
                if 'sample2' in files.keys():
                    naam = 'sample2'
                    formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/Formats/')
                    handle_uploaded_file(os.path.join(formatpath,filelist[naam]),files[naam])
                    messages.success(request, 'Sample 2 updated.')
                if 'sample3' in files.keys():
                    naam = 'sample3'
                    formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/Formats/')
                    handle_uploaded_file(os.path.join(formatpath,filelist[naam]),files[naam])
                    messages.success(request, 'Sample 3 updated.')
                return control_panel(request)
            else:
                return control_panel(request)
    else:
        return oops(request)

def TESG_upload(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            if not 'adminpassT' in req.keys():
                messages.error(request, 'Enter Administrator password.')
                return control_panel(request)
            adminpassF = req['adminpassT']
            if not check_password(adminpassF,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return control_panel(request)
            
            if request.FILES:
                tesgnum = req['tesgnum']
                tesgdate = req['tesgdate']
                projids = req['projids']
                tesgpath = ''
                files = request.FILES
                if 'momupload' in files.keys():
                    mompload = files['momupload']
                    naam = 'TESG_'+tesgnum + '.'+mompload.name.split('.')[1]
                    tesgpath =os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Admin/TESG/')
                    if smkdir(tesgpath):
                        tesgpath = os.path.join(tesgpath, naam)
                        handle_uploaded_file(tesgpath,files['momupload'])
                    else:
                        return oops(request)
                allTESG = TESG_admin.objects.values_list('TESG_no')
                # print(allTESG.TESG_no)
                for TESGnum in allTESG:
                    print(TESGnum)
                    if int(tesgnum) in TESGnum:
                        messages.error(request, 'ERROR! TESG number '+ tesgnum +' entry already exists')
                        return control_panel(request)
                TESG_admin1 = TESG_admin()
                TESG_admin1.TESG_no = tesgnum
                TESG_admin1.filepath = tesgpath
                TESG_admin1.TESG_date = tesgdate
                TESG_admin1.projects = projids
                TESG_admin1.save()
                tesgprojs = projids.split(',')
                allprojs = projects.objects.all()
                for proj in allprojs:
                    if str(proj.id) in tesgprojs:
                        projectid = projects.objects.get(id = proj.id)
                        if projectid.tesg_list:
                            projectid.tesg_list = str(projectid.tesg_list) +',' + str(tesgnum)
                        else:
                            projectid.tesg_list = str(tesgnum)
                        projectid.save(update_fields=['tesg_list'])
                messages.success(request, 'New TESG number: '+tesgnum+' added.')
                return control_panel(request)
        else:
            return oops(request)
    else:
        return oops(request)