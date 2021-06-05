from .helpers import *


def admin_project_details(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        context['proj'] = projects.objects.get(id = projectid)
        return render(request, 'psdf_main/_admin_project_details.html', context)
    else:
        return oops(request)