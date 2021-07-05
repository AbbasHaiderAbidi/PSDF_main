from .helpers import *

def monitoring_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_monitoring_projects.html', context)
    else:
        return oops(request)

    
def approve_monitoring(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            if not Appraisal_admin.objects.filter(projid = projectid)[:1].get():
                messages.success(request, 'Aborted! No entry regarding Monitoring exists.')
                return redirect('/monitoring_projects/')
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projectid)
                project.status = '4'
                project.workflow = project.workflow + ']*[' + 'Project approved in Monitoring Phase on '+ datetime.now()
                project.save(update_fields=['status'])
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
        thisproject.workflow = thisproject.workflow + ']*[' + 'Project reverted back to Appraisal phase from Monitoring phase on ' + datetime.now()
        thisproject.save(update_fields = ['status','workflow'])
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to Appraisal from Monitoring phase')
        messages.success(request, 'Project '+ thisproject.name +' sent back to Appraisal.')
        return redirect('/monitoring_projects')
    else:
        return oops(request)


def send_to_tesg(request, projid):
    if adminonline(request):
        thisproject = projects.objects.get(id = projid)
        thisproject.status = '1'
        thisproject.workflow = thisproject.workflow + ']*[' + 'Project reverted back to TESG phase from Monitoring phase on ' + datetime.now()
        thisproject.save(update_fields = ['status','workflow'])
        notification(thisproject.userid.id, 'Project '+ thisproject.name +' sent back to TESG from Monitoring phase')
        messages.success(request, 'Project '+ thisproject.name +' sent back to Appraisal.')
        return redirect('/monitoring_projects')
    else:
        return oops(request)