from .helpers import *

def underexamination(request):
    if useronline(request):
        
        user = userDetails(request.session['user'])
        userobj = users.objects.get(id = user['id'])
        projectobj = projects.objects.filter(userid = userobj, status = '1')
        context = {'user' : user, 'projectobj': projectobj}
        return render(request, 'psdf_main/under_examination.html', context)
    else:
        return oops(request)