from .helpers import *

def monitoring_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        print(context['monitoring_projects'])
        return render(request, 'psdf_main/_admin_monitoring_projects.html', context)
    else:
        return oops(request)

    
def approve_monitoring(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projectid)
                project.status = '4'
                moniaprdate = datetime.now().date()
                project.workflow = str(project.workflow) + ']*[' + 'Project approved in Monitoring Phase on '+ str(moniaprdate)
                project.moniaprdate = moniaprdate
                project.save(update_fields=['status','moniaprdate', 'workflow'])
                messages.success(request, 'Project : '+ project.name + ' has been approved Appraisal Committee.')
                notification(projects.objects.get(id = projectid).userid.id, 'Project ID: '+ projectid +' has been approved by Appraisal committee')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            return redirect('/monitoring_projects/')
        else:
            return oops(request)
    else:
        return oops(request)


def send_to_appr(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '2'
        thisproject.workflow = str(thisproject.workflow) + ']*[' + 'Project reverted back to Appraisal phase from Monitoring phase on ' + str(datetime.now().date())
        thisproject.moniaprdate = None
        thisproject.appraprdate = None
        thisproject.save(update_fields = ['status','workflow','moniaprdate','appraprdate'])
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to Appraisal from Monitoring phase')
        messages.success(request, 'Project '+ thisproject.name +' sent back to Appraisal.')
        return redirect('/monitoring_projects')
    else:
        return oops(request)


def msend_to_tesg(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '1'
        thisproject.workflow = str(thisproject.workflow) + ']*[' + 'Project reverted back to TESG phase from Monitoring phase on ' + str(datetime.now().date())
        thisproject.moniaprdate = None
        thisproject.appraprdate = None
        thisproject.tesgaprdate = None
        thisproject.save(update_fields = ['status','workflow','moniaprdate','appraprdate','tesgaprdate'])
        
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to TESG from Monitoring phase')
        messages.success(request, 'Project '+ thisproject.name +' sent back to TESG phase.')
        return redirect('/monitoring_projects')
    else:
        return oops(request)