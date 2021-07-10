from .helpers import *

def user_monitoring_projects(request):
    if useronline(request):
        context = full_user_context(request)
        # context['monitoring_projects'] = Monitoring_admin.objects.filter(userid = users.objects.get(id = userDetails(request.session['user'])['id']))
        return render(request, 'psdf_main/_user_monitoring_projects.html', context)
    else:
        return oops(request)