from .helpers import *


def appraisal_projects(request):
    if adminonline(request):
        context = full_admin_context(request)
        return render(request, 'psdf_main/_admin_appraisal_projects.html', context)
    else:
        return oops(request)
    
def approve_appraisal(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        if request.method == 'POST':
            req = request.POST
            adminpass = req['adminpass']
            if check_password(adminpass,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = projid)
                project.status = '3'
                project.save(update_fields=['status'])
                messages.success(request, 'Project : '+ project.name + ' has been approved Appraisal Committee.')
                notification(projects.objects.get(id = projid).userid.id, 'Project ID: '+projid+' has been approved by Appraisal committee')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            
            return redirect('/TESG_projects/')
        else:
            return oops(request)
    else:
        return oops(request)