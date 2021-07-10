from .helpers import *

def under_examination(request):
    if useronline(request):
        context = full_user_context(request)
        userobj = users.objects.get(id = context['user']['id'])
        projectobj = temp_projects.objects.filter(userid = userobj, deny = False)
        context['projectobj']= projectobj
        context['noprojobj']= projectobj.count()
        context['proj_boqlist'] = getTempProjects_user(request, userobj)
        return render(request, 'psdf_main/_user_under_examination.html', context)
    else:
        return oops(request)