from .helpers import *

def user_appraisal_projects(request):
    if useronline(request):
        context = full_user_context(request)
        print(context['appraisal_projects'])
        context['appraisal_projs'] = Appraisal_admin.objects.filter(userid = userDetails(request.session['user'])['id'])
        return render(request, 'psdf_main/_user_appraisal_projects.html', context)
    else:
        return oops(request)
    
    
def user_appraisal_report(request, projid):
    print(projects.objects.get(id = projid).userid.username)
    if useronline(request) and request.session['user'] == projects.objects.get(id = projid).userid.username:
        context = full_user_context(request)
        filepath = Appraisal_admin.objects.filter(projid = projid)[:1].get().filepath
        if os.path.exists(filepath):
            return handle_download_file(filepath, request)
        else:
            messages.error(request, 'File does not exists')
            return redirect('/user_appraisal_projects')
    else:
        return oops(request)