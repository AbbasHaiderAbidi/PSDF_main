from .helpers import *

def acceptdpr(request, projid):
    if adminonline(request):
        if request.POST:
            req = request.POST
            fundcategory = req['fundcategory'+projid]
            quantum = req['quantum'+projid]
            acceptdate = req['acceptdate'+projid]
            remark = ''
            if req['remark'+projid]:
                remark = req['remark'+projid]
            adminpass = req['adminpass'+projid]
            temp_proj = temp_projects.objects.get(id = projid)
            checkingpass = users.objects.filter(username = request.session['user'])[:1].values('password')[0]['password']
            if not check_password(adminpass,checkingpass):
                messages.error(request, 'Invalid admin password, acceptance of project: '+temp_proj.proname+' ABORTED.')
                return redirect('/admin_pending_projects')
            
            newproject = projects()
            newproject.name = temp_proj.proname
            newproject.dprsubdate = temp_proj.dprsubdate
            newproject.dpraprdate = acceptdate
            newproject.amt_asked = temp_proj.amountasked
            newproject.schedule = temp_proj.schedule
            newproject.fundcategory = fundcategory
            # newproject.projectpath = newprojectpath
            newproject.quantumOfFunding = quantum
            newproject.userid = temp_proj.userid
            
            if not remark == '':
                newproject.remark = remark
            newproject.submitted_boq = temp_proj.submitted_boq
            newproject.save()
            newentry = projects.objects.filter(name = temp_proj.proname, amt_asked = temp_proj.amountasked, userid = temp_proj.userid, schedule = temp_proj.schedule, dprsubdate = temp_proj.dprsubdate)[0]
            newpath = '/'.join(temp_proj.projectpath.split('/')[:-2])+'/'+ str(newentry.id)
            if smkdir(newpath):
                for f in glob.glob(temp_proj.projectpath+'/*'):
                    os.replace(f,os.path.join(newpath , f.split('/')[-1]))
                newentry.projectpath = newpath
                newentry.save(update_fields=['projectpath'])
                temp_projects.objects.get(id=temp_proj.id).delete()
                srmdir(temp_proj.projectpath)
                projectobj = getTempProjects(request)
                project_user = users.objects.get(id = temp_proj.userid.id)
                project_user.notification = str(project_user.notification) + ']*[' + 'Your project : '+ newentry.name +' has been accepted with project ID:' + str(newentry.id)
                project_user.save(update_fields=['notification'])
                context = {'user':userDetails(request.session['user']), 'projectobj' : projectobj, 'nopendingusers' : pen_users_num(request), 'nopendingprojects' : len(projectobj) }
                messages.error(request, 'Project: '+newentry.name+' has been successfully accepted with ID: '+str(newentry.id)+'.')
                return render(request, 'psdf_main/_admin_pending_projects.html', context)

            else:
                print("Error Creating directory")
                context = {'user':userDetails(request.session['user']), 'projectobj' : projectobj, 'nopendingusers' : pen_users_num(request), 'nopendingprojects' : len(projectobj) }
                messages.error(request, 'Error creating a record.')
                return render(request, 'psdf_main/_admin_pending_projects.html', context)
            return oops(request)
        else:
            return oops(request)
    else:
        return oops(request)


def rejectdpr(request, projid):
    if adminonline(request):
        if request.POST:
            req = request.POST
            rejectdate = req['rejectdate'+projid]
            rremark = req['rremark'+projid]
            radminpass = req['radminpass'+projid]
            temp_proj = temp_projects.objects.get(id = projid)
            checkingpass = users.objects.filter(username = request.session['user'])[:1].values('password')[0]['password']
            if not check_password(radminpass,checkingpass):
                messages.error(request, 'Invalid admin password, acceptance of project: '+temp_proj.proname+' ABORTED.')
                return redirect('/admin_pending_projects')
            temp_proj.dprdenydate = rejectdate
            temp_proj.deny = True
            temp_proj.remark = rremark
            temp_proj.save(update_fields=['dprdenydate','deny','remark'])
            messages.success(request, 'Project : '+ temp_proj.proname + ' has been rejected.')
            return redirect('/admin_pending_projects')
    else:
        return oops(request)


def download_temp_project(request, projid):
    if adminonline(request):
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            type_n_id = projid.split('_')
            file_type = type_n_id[0]
            proid = type_n_id[1]
            temp_proj_path = temp_projects.objects.get(id = proid).projectpath
            # print(file_type)
            # print(glob.glob(temp_proj_path+'/'+filelist[file_type]+'*'))
            filepath = os.path.join(glob.glob(temp_proj_path+'/'+filelist[file_type]+'*')[0])
            print(filepath)
            if os.path.exists(filepath):
                with open(filepath,'rb') as fh:
                    response = HttpResponse(fh.read(), content_type = "application/adminupload")
                    response['Content-Disposition'] = 'inline;filename =' + filepath.split('/')[-1]
                    return response
        else:
            return oops(request)
    else:
        return oops(request)
