from .helpers import *
# Create your views here.


def admin_dashboard(request):
    if adminonline(request):
        return render(request, 'psdf_main/_admin_dashboard.html')
    else:
        return redirect('')

    
def admin_users(request):
    user = userDetails(request.session['user'])
    nopendingprojects = len(getTempProjects(request))
    nopendingusers = pen_users_num(request)
    if not nopendingusers:
        nopendingusers = 0
    if not nopendingprojects:
        nopendingprojects = 0
        
    context = {'allusers' : get_all_users(request), 'user':user, 'userobj' : pen_users(request), 'nopendingusers' : nopendingusers, 'nopendingprojects' : nopendingprojects }
    return render(request, 'psdf_main/_admin_users.html', context)


def admin_pending_users(request):
    if adminonline(request):
        user = userDetails(request.session['user'])
        nopendingprojects = len(getTempProjects(request))
        nopendingusers = pen_users_num(request)
        if not nopendingusers:
            nopendingusers = 0
        if not nopendingprojects:
            nopendingprojects = 0
        context = {'user':user, 'userobj' : pen_users(request), 'nopendingusers' : nopendingusers, 'nopendingprojects' : nopendingprojects }
        return render(request, 'psdf_main/_admin_pending_users.html', context)


def admin_pending_projects(request):
    if adminonline(request):
        user = userDetails(request.session['user'])
        
        context = {'user':user, 'projectobj' : getTempProjects(request), 'nopendingusers' : pen_users_num(request), 'nopendingprojects' : len(getTempProjects(request)) }
        return render(request, 'psdf_main/_admin_pending_projects.html', context)
    
def approve_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.aprdate = datetime.now()
        user.activate = True
        user.admin = False
        user.active = True
        user.lastlogin = user.aprdate
        user.save(update_fields=['lastlogin','aprdate','activate','admin','active'])
        user1 = userDetails(request.session['user'])
        context = {'user':user1,'userobj':pen_users(request), 'nopendingusers' : pen_users_num(request)}
        messages.error(request, 'User ' + user.username + ' has been approved.')
        return render(request, 'psdf_main/_admin_pending_users.html', context)
    else:
        return oops(request)
    
def reject_user(request, userid):
    if adminonline(request):
        userreject = users.objects.get(id=userid)
        usernamereject = userreject.username
        userreject.delete()
        user = userDetails(request.session['user'])
        context = {'user':user,'userobj':pen_users(request), 'nopendingusers' : pen_users_num(request)}
        messages.error(request, 'User ' + usernamereject + ' has been Rejected.')
        return render(request, 'psdf_main/_admin_pending_users.html', context)
    else:
        return oops(request)
    
def allow_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.admin = False
        user.active = True
        user.save(update_fields=['admin','active'])
        user1 = userDetails(request.session['user'])
        context = {'allusers' : get_all_users(request),'user':user1, 'userobj' : pen_users(request), 'nopendingusers' : pen_users_num(request) }
        messages.success(request, 'User ' + user.username + ' has been allowed.')
        return render(request, 'psdf_main/_admin_users.html', context)
    else:
        return oops(request)

def ban_user(request, userid):
    if adminonline(request):
        user = users.objects.get(id = userid)
        user.admin = False
        user.active = False
        user.save(update_fields=['admin','active'])
        user1 = userDetails(request.session['user'])
        context = {'allusers' : get_all_users(request),'user':user1, 'userobj' : pen_users(request), 'nopendingusers' : pen_users_num(request) }
        messages.error(request, 'User ' + user.username + ' has been banned.')
        return render(request, 'psdf_main/_admin_users.html', context)
    else:
        return oops(request)

def download_temp_project(request, projid):
    return oops(request)

def approve_project(request, projid):
    return oops(request)

def reject_project(request, projid):
    return oops(request)