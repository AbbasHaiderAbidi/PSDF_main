from .helpers import *




def TESG_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_TESG_projects.html', context)
    else:
        return oops(request)

def tesg_context(request, project_id):
    context = full_admin_context(request)
    context['proj'] = projects.objects.get(id = project_id)
    try:
        context['tesg_list'] = projects.objects.get(id = project_id).tesg_list.split(',')
    except :
        context['tesg_list'] =  ''
    context['proj_tesg'] = TESG_master.objects.filter(project = context['proj'])
    
    return context

def TESG_chain(request, project_id):
    if adminonline(request):
        context = tesg_context(request, project_id)
        return render(request, 'psdf_main/_admin_TESG.html', context)
    else:
        return oops(request)
    
    
def tesgchain_form(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            tesgnum = req['tesgnum']
            tesg_outcome = req['tesg_outcome']
            adminpass = req['adminpass']
            tesgpath = ""
            projid = req['projid']
            context = full_admin_context(request)
            context['proj'] = projects.objects.get(id = projid)
            try:
                context['tesg_list'] = projects.objects.get(id = projid).tesg_list.split(',')
            except :
                context['tesg_list'] =  ''
            context['proj_tesg'] = TESG_master.objects.filter(project = context['proj'])
            alreadyactive = False
            activetesg = TESG_master.objects.filter(project = projects.objects.get(id = projid), active = True)
            print(activetesg)
            if activetesg.exists():
                alreadyactive = True
            print(alreadyactive)
            if alreadyactive:
                messages.error(request, 'Already a TESG chain is active, please wait.')
                return redirect('/TESG_chain/'+projid)
            if TESG_master.objects.filter(tesgnum = TESG_admin.objects.filter(TESG_no = tesgnum)[:1].get()):
                messages.error(request, 'TESG entry already made.')
                return redirect('/TESG_chain/'+projid)
            if 'observations' in request.FILES:
                print("file1")
                observations = request.FILES['observations']
                tesgpath = projects.objects.get(id = projid).projectpath + '/TESG/'
                smkdir(tesgpath)
                print("file2")
                try:
                    extension = str(observations.name.split(".")[1])
                    print("file3")
                except:
                    extension = ''
                    print("file4")
                handle_uploaded_file(os.path.join(tesgpath,str(str(tesgnum) + "." +extension )),observations)
                print("file5")
            tesg = TESG_master()
            tesg.project = projects.objects.get(id = projid)
            tesg.tesgnum = TESG_admin.objects.filter(TESG_no = tesgnum)[:1].get()
            tesg.admin_outcome = tesg_outcome
            tesg.admin_filepath = tesgpath
            tesg.save()
            
            messages.error(request, 'Outcome of TESG '+tesgnum+' have been intimated to the user.')
            notification(str(tesg.project.userid.id), 'TESG #'+tesgnum+' updated for project ID : '+str(tesg.project.id))
            return redirect('/TESG_chain/'+projid)
        
    else:
        return oops(request)
    
    
def acceptTESG(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            tesgnum = req['tesgnum']
            adminpass = req['adminpass']
            userid = req['userid']
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/TESG_chain/'+projid)
            else:
                tesg = TESG_master.objects.get(id = get_TESG_id(request,tesgnum, projid))
                tesg.accepted = True
                tesg.rejected = False
                tesg.active = False
                tesg.save(update_fields=['accepted','rejected','active'])
                notification(userid, 'Response for TESG : '+tesgnum+', project ID: '+projid+ ' has been Accepted.')
                messages.error(request, 'Response for TESG number '+tesgnum+' accepted.')
                return redirect('/TESG_chain/'+projid)
    else:
        return oops(request)


def rejectTESG(request):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            tesgnum = req['tesgnum']
            adminpass = req['adminpass']
            remarks = req['remarks']
            userid = req['userid']
            if not check_password(adminpass,userDetails(request.session['user'])['password']):
                messages.error(request, 'Invalid Administrator password.')
                return redirect('/TESG_chain/'+projid)
            else:
                tesg = TESG_master.objects.get(id = get_TESG_id(request,tesgnum, projid))
                tesg.rejected = True
                tesg.accepted = False
                tesg.active = False
                pro = projects.objects.get(id = projid)
                pro.remark = remarks
                pro.save(update_fields=['remark'])
                tesg.save(update_fields=['accepted','rejected','active'])
                notification(userid, 'Response for TESG : '+tesgnum+', project ID: '+projid+ ' has been Rejected.')
                messages.error(request, 'Response for TESG number '+tesgnum+' Rejected.')
                return redirect('/TESG_chain/'+projid)
    else:
        return oops(request)
    
def downloadTESGresponse(request, tesgid_projid):
    if adminonline(request):
        tesgstr = tesgid_projid.split('_')
        tesgnum = tesgstr[0]
        tesgid = tesgstr[1]
        projid = tesgstr[2]
        
        tesgpath = TESG_master.objects.get(id = tesgid).user_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        try:
            filepath = os.path.join(glob.glob(tesgpath+'/'+str(tesgnum)+'_response'+'*')[0])
        except :
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        return handle_download_file(filepath, request)
            
def downloadTESGrequest(request, tesgid_projid):
    if adminonline(request):
        tesgstr = tesgid_projid.split('_')
        tesgnum = tesgstr[0]
        tesgid = tesgstr[1]
        projid = tesgstr[2]

        tesgpath = TESG_master.objects.get(id = tesgid).admin_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        try:
            filepath = os.path.join(glob.glob(tesgpath+'/'+str(tesgnum)+'*')[0])
        except :
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        return handle_download_file(filepath, request)
    else:
        return oops(request)

def approveTESG(request, projid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            activeTESG = TESG_master.objects.filter(project = projects.objects.get(id = projid), active = True)
            aretheretesg = TESG_master.objects.filter(project = projects.objects.get(id = projid))
            
            if activeTESG:
                messages.error(request, 'A TESG chain is active for this project.')
                return redirect('/TESG_projects/')
            
            if not aretheretesg:
                messages.error(request, 'No TESG has been submitted for this project.')
                return redirect('/TESG_projects/')
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projid)
                project.status = '2'
                project.workflow = str(project.workflow) + ']*[' + 'Project approved in TESG phase on '+ str(datetime.now())
                project.save(update_fields=['status','workflow'])
                messages.success(request, 'Project : '+ project.name + ' has been approved in TESG phase.')
                notification(projects.objects.get(id = projid).userid.id, 'Project ID: '+projid+' has been approved in TESG phase')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            
            return redirect('/TESG_projects/')
        else:
            return oops(request)
    else:
        return oops(request)