from .helpers import *


def appraisal_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        context['appr_admin'] = Appraisal_admin.objects.values_list('projid', flat = True).all()[:]
        # print(context['appr_admin'])
        # context['appr_projects'] = Appraisal_admin.objects.all()
        return render(request, 'psdf_main/_admin_appraisal_projects.html', context)
    else:
        return oops(request)
    
def approve_appraisal(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            if not Appraisal_admin.objects.filter(projid = projectid)[:1].get():
                messages.success(request, 'Aborted! No entry regarding appraisal exists.')
                return redirect('/appraisal_projects/')
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projectid)
                project.status = '3'
                project.workflow = project.workflow + ']*[' + 'Project approved in Appraisal phase on '+ datetime.now()
                project.save(update_fields=['status'])
                messages.success(request, 'Project : '+ project.name + ' has been approved Appraisal Committee.')
                notification(projects.objects.get(id = projectid).userid.id, 'Project ID: '+projectid+' has been approved by Appraisal committee')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            
            return redirect('/appraisal_projects/')
        else:
            return oops(request)
    else:
        return oops(request)


    ###MAKE appraisal entry
    
def update_appraisal(request, projid):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            apprdate = req['apprdate']
            adminpass = req['adminpass']
            remarks = req['remarks']
            appr_path = ''
            appr = Appraisal_admin.objects.filter(projid = projid)[:1].get()
            removed = sremove(appr.filepath)
            
            if 'observations' in request.FILES:
                observations = request.FILES['observations']
                apprpath = projects.objects.get(id = projid).projectpath + '/Appraisal/'
                smkdir(apprpath)
                try:
                    extension = str(observations.name.split(".")[1])
                except:
                    extension = ''
                appr_path = os.path.join(apprpath,str(projid+'_'+'Appraisal'+ "." +extension ))
                handle_uploaded_file(appr_path,observations)
            
            thisproj = projects.objects.get(id = projid)
            appr.project = thisproj
            appr.projid = projid
            appr.filepath = appr_path
            appr.appr_date = apprdate
            appr.remarks = remarks
            appr.save(update_fields = ['project','projid','filepath','appr_date', 'remarks'])
            messages.success(request, 'Appraisal entry for project ID: '+projid+' updated.')
            notification(thisproj.userid.id, 'Appraisal entry for project ID: '+projid+' updated.')
            return redirect('/appraisal_projects/')
    else:
        return oops(request)
    
    
def create_appraisal(request, projid):
    if adminonline(request):
        if request.method == 'POST':
            req = request.POST
            apprdate = req['apprdate']
            adminpass = req['adminpass']
            remarks = req['remarks']
            appr_path = ''
            if 'observations' in request.FILES:
                observations = request.FILES['observations']
                apprpath = projects.objects.get(id = projid).projectpath + '/Appraisal/'
                smkdir(apprpath)
                try:
                    extension = str(observations.name.split(".")[1])
                except:
                    extension = ''
                appr_path = os.path.join(apprpath,str(projid+'_'+'Appraisal'+ "." +extension ))
                handle_uploaded_file(appr_path,observations)
            appr = Appraisal_admin()
            thisproj = projects.objects.get(id = projid)
            appr.project = thisproj
            appr.projid = projid
            appr.filepath = appr_path
            appr.userid = users.objects.get(id = users.objects.filter(username = request.session['user'])[:1].get())
            appr.appr_date = apprdate
            appr.remarks = remarks
            appr.save()
            messages.success(request, 'Appraisal entry for project ID: '+projid+' created.')
            notification(thisproj.userid.id, 'Appraisal entry for project ID: '+projid+' created.')
            return redirect('/appraisal_projects/')
    else:
        return oops(request)
    
def delete_appr_doc(request, projid):
    if adminonline(request):
        thisproject = Appraisal_admin.objects.filter(projid = projid)[:1].get()
        filepathway = thisproject.filepath
        thisproject.filepath = ''
        thisproject.save(update_fields = ['filepath'])
        if sremove(filepathway):
            messages.error(request, 'File removed successfully')
            return redirect('/appraisal_projects/')
        else:
            messages.error(request, 'Unable to remove the file.')
            return redirect('/appraisal_projects/')
        
    else:
        return oops(request)
    
def send_to_tesg(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '1'
        thisproject.workflow = thisproject.workflow + ']*[' + 'Reverted back to TESG by Appraisal committee on ' + datetime.now()
        thisproject.save(update_fields = ['status', 'workflow'])
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to TESG by PSDF Sectt.')
        messages.success(request, 'Project '+ thisproject.name +' sent back to TESG.')
        return redirect('/appraisal_projects')
    else:
        return oops(request)