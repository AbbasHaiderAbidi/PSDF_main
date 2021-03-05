from .helpers import *



def control_panel(request):
    if adminonline(request):
        user = userDetails(request.session['user'])
        nopendingusers = pen_users_num(request)
        if not nopendingusers:
            nopendingusers = 0
        context = {'allusers' : get_all_users(request), 'user':user, 'userobj' : pen_users(request), 'nopendingusers' : nopendingusers, 'nopendingprojects' : len(getTempProjects(request)) }
        return render(request, 'psdf_main/_admin_control_panel.html', context)
    else:
        return oops(request)
    
    
def uploadformat(request):
    filelist = {'support':'DPR_Supporting_documents.zip', 'format':'DPR_Forms.zip','sample1':'sample1.zip','sample2':'sample2.zip','sample3':'sample3.zip'}
    if adminonline(request):
        if request.method == 'POST':
            if request.FILES:
                
                formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Formats/')
                handle_uploaded_file(os.path.join(formatpath,filelist[filename]),dpr)
    else:
        return oops(request)