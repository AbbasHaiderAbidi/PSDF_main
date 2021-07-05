from .helpers import *


def user_tesg(request):
    if useronline(request):
        context = full_user_context(request)
        return render(request, 'psdf_main/_user_TESG_projects.html', context)
    else:
        return oops(request)
    
def user_TESG_chain(request, projid):
    if useronline(request):
        if proj_of_user(request, projid):
            context = full_user_context(request)
            context['proj'] = projects.objects.get(id = projid)
            context['proj_tesg'] = TESG_master.objects.filter(project = context['proj'])
            context['current_tesg'] = TESG_master.objects.filter(project = context['proj'])[:1].get()
            return render(request, 'psdf_main/_user_TESG.html', context)
        else:
            return oops(request)
    else:
        return oops(request)

def user_tesg_response(request):
    if useronline(request):
        if request.method == 'POST':
            req = request.POST
            projid = req['projid']
            tesg_no = req['tesg_no']
            userpass = req['userpass']
            tesg_response = req['tesg_response']
            if proj_of_user(request, projid):
                if not check_password(userpass,userDetails(request.session['user'])['password']):
                    messages.error(request, 'Invalid Administrator password.')
                    return user_TESG_chain(request, projid)
                
                admin_tesg = TESG_admin.objects.filter(TESG_no = tesg_no)[:1].get()
                admin_project = projects.objects.filter(id = projid)[:1].get()
                this_tesg = TESG_master.objects.filter(project = admin_project, tesgnum = admin_tesg, active = True)[:1].get()
                tesgpath = ''
                if 'responses' in request.FILES:
                        responses = request.FILES['responses']
                        tesgpath = projects.objects.get(id = projid).projectpath + '/TESG/'
                        smkdir(tesgpath)
                        print("file2")
                        try:
                            extension = str(responses.name.split(".")[1])
                        except:
                            extension = ''
                        handle_uploaded_file(os.path.join(tesgpath,str(str(tesg_no)+'_response'+ "." +extension )),responses)
                        
                this_tesg.user_res_date = datetime.now()
                this_tesg.user_response = tesg_response
                this_tesg.user_filepath = tesgpath
                this_tesg.save(update_fields=['user_res_date','user_response','user_filepath'])
                messages.error(request, 'Response of TESG '+tesg_no+' have been intimated to PSDF Sectt.')
                notification(users.objects.filter(admin = True)[:1].get().id, 'TESG #'+tesg_no+' response updated by user '+request.session['user'])
                return user_TESG_chain(request, projid)
            else:
                return oops(request)
        else:
            return oops(request)


def download_tesg_user_outcome(request, tesg_str):
    if useronline(request):
        tesgstr = tesg_str.split('_')
        tesgnum = tesgstr[0]
        tesgid = tesgstr[1]
        projid = tesgstr[2]
        username = TESG_master.objects.get(id = tesgid).project.userid.username
        if not username == request.session['user']:
            return oops(request)
        
        tesgpath = TESG_master.objects.get(id = tesgid).admin_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        try:
            filepath = os.path.join(glob.glob(tesgpath+'/'+str(tesgnum)+'.*')[0])
        except :
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        return handle_download_file(filepath, request)
    else:
        return oops(request)
    
def download_tesg_user_response(request, tesg_str):
    if useronline(request):
        tesgstr = tesg_str.split('_')
        tesgnum = tesgstr[0]
        tesgid = tesgstr[1]
        projid = tesgstr[2]
        username = TESG_master.objects.get(id = tesgid).project.userid.username
        if not username == request.session['user']:
            return oops(request)
        
        tesgpath = TESG_master.objects.get(id = tesgid).user_filepath
        if tesgpath == '' or tesgpath == None:
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        try:
            filepath = os.path.join(glob.glob(tesgpath+'/'+str(tesgnum)+'_response.*')[0])
        except :
            messages.error(request, 'Function is not available.')
            return redirect('/TESG_chain/'+projid)
        return handle_download_file(filepath, request)
    else:
        return oops(request)