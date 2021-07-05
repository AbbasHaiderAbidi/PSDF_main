from .helpers import *

def user_monitoring_projects(request):
    if useronline(request):
        context = full_user_context(request)
        return render(request, 'psdf_main/_user_monitoring_projects.html', context)
    else:
        return oops(request)