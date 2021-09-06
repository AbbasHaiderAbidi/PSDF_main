from .helpers import *


def new_loa(request):
    if useronline(request):
        context = full_user_context(request)
        if request.method == 'POST':
            req = request.POST
            projid = req.get('projectid')
            thisproject = projects.objects.get(id = projid)
            aboq = boqdata.objects.filter(project = thisproject, boqtype = '2')
            context['aboq'] = aboq
            context['approved_boq_total'] = boq_grandtotal(aboq)
            context['loa_project'] = thisproject
            return render(request, 'psdf_main/_user_new_loa.html', context)
        userobj = users.objects.filter(username = request.session['user'])[:1].get()
        print(userobj)
        context['projectlist'] = projects.objects.filter(status = '4', userid = userobj)
        print(context['projectlist'])
        return render(request, 'psdf_main/_user_new_loa.html', context)
    else:
        return oops(request)
    
