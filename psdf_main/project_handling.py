from .helpers import *

def acceptdpr(request, projid):
    if adminonline(request):
        if request.POST:
            req = request.POST
            fundcategory = req['fundcategory'+projid]
            quantum = req['quantum'+projid]
            # acceptdate = req['acceptdate'+projid]
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
            # newproject.dpraprdate = acceptdate
            newproject.amt_asked = temp_proj.amountasked
            newproject.schedule = temp_proj.schedule
            newproject.fundcategory = fundcategory
            # newproject.projectpath = newprojectpath
            newproject.quantumOfFunding = quantum
            newproject.amt_approved = (float(quantum)/100)*float(temp_proj.amountasked)
            newproject.userid = temp_proj.userid
            newproject.tesglist = ''
            if not remark == '':
                newproject.remark = remark
            newproject.submitted_boq = temp_proj.submitted_boq
            newproject.workflow = 'DPR accepted on '+ str(datetime.now())
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
                context = full_admin_context(request)
                messages.error(request, 'Project: '+newentry.name+' has been successfully accepted with ID: '+str(newentry.id)+'.')
                return render(request, 'psdf_main/_admin_pending_projects.html', context)

            else:
                print("Error Creating directory")
                context = full_admin_context(request)
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
            rremark = req['rremark'+projid]
            radminpass = req['radminpass'+projid]
            temp_proj = temp_projects.objects.get(id = projid)
            checkingpass = users.objects.filter(username = request.session['user'])[:1].values('password')[0]['password']
            if not check_password(radminpass,checkingpass):
                messages.error(request, 'Invalid admin password, acceptance of project: '+temp_proj.proname+' ABORTED.')
                return redirect('/admin_pending_projects')
            temp_proj.deny = True
            temp_proj.remark = rremark
            
            temp_proj.save(update_fields=['dprdenydate','deny','remark'])
            messages.success(request, 'Project : '+ temp_proj.proname + ' has been rejected.')
            return redirect('/admin_pending_projects')
    else:
        return oops(request)


def download_temp_project(request, projid):
    try:
        type_n_id = projid.split('_')
        file_type = type_n_id[0]
        proid = type_n_id[1]
    except:
        return oops(request)
    print(temp_projects.objects.get(id = proid).userid.username)
    print(request.session['user'])
    if (adminonline(request) or (temp_projects.objects.get(id = proid).userid.username == request.session['user'])):
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            proj_path = temp_projects.objects.get(id = proid)
            if proj_path :
                proj_path = proj_path.projectpath
                filepath = os.path.join(glob.glob(proj_path+'/'+filelist[file_type]+'*')[0])
                return handle_download_file(filepath, request)
    return oops(request)

def download_project(request, projid):
    try:
        type_n_id = projid.split('_')
        file_type = type_n_id[0]
        proid = type_n_id[1]
    except:
        return oops(request)

    if (adminonline(request) or (projects.objects.get(id = proid).userid.username == request.session['user'])):
        user = userDetails(request.session['user'])
        if projid:
            filelist = {'DPR':'DPR', 'forms':'forms','otherdocs':'otherdocs'}
            proj_path = projects.objects.get(id = proid)
            if proj_path :
                proj_path = proj_path.projectpath
                filepath = os.path.join(glob.glob(proj_path+'/'+filelist[file_type]+'*')[0])
                handle_download_file(filepath, request)
    return oops(request)


def rejectproject(request, projid):
    pages = {'TESG':'/TESG_projects', 'Appraisal':'/appraisal_projects'}
    if adminonline(request):
        context = full_admin_context(request)
        if request.POST:
            page_id = projid.split('_')
            proid = page_id[1]
            page = page_id[0]
            req = request.POST
            denydate = req['rejectdate'+proid]
            remark = req['rremark'+proid]
            radmin = req['radminpass'+proid]
            if remark == '':
                messages.success(request, 'Aborted! Remarks cannot be empty')

            activeTESG = TESG_master.objects.filter(project = projects.objects.get(id = proid), active = True)
            if activeTESG:
                messages.success(request, 'A TESG chain is active for this project.')
                return redirect('/TESG_projects/')

            if check_password(radmin,users.objects.get(id = context['user']['id']).password):
                project = projects.objects.get(id = proid)
                project.deny = True
                project.denydate = denydate
                project.remark = remark
                project.workflow = str(project.workflow) + ']*[' + 'Project rejected on ' + denydate
                project.save(update_fields=['denydate' , 'deny' , 'remark' , 'workflow'])
                messages.success(request, 'Project : ' + project.name + ' has been rejected.')
                notification(projects.objects.get(id = projid).userid.id, 'Project ID: '+projid+' has been rejected in '+page+' phase')
            else:
                messages.success(request, 'Aborted! Invalid administrator password.')
            return redirect(pages[page])
        else:
            return oops(request)
    else:
        return oops(request)
    
    
def update_boq(request, projectid):
    if adminonline(request):
        context = full_admin_context(request)
        
        projid = projectid
        
        if request.method == 'POST':
            req = request.POST
            nitem = req['nitem']
            projid = req['projid']
            boq_project = projects.objects.get(id = projid)
            if not boq_project:
                messages.warning(request, 'Project does not exist.')
                return redirect('/update_boq/0')
            boq = []
            for i in range(1,1000):
                if not (req['itemname'+str(i)] == ''):
                    itemqty = req['itemqty'+str(i)]
                    itemprice = req['itemprice'+str(i)]
                    if isfloat(itemqty) and float(itemprice):
                        boq.append({'itemname':req['itemname'+str(i)],'itemno':req['itemno'+str(i)],'itemdesc': req['itemdesc'+str(i)], 'itemqty': itemqty, 'itemprice': itemprice, 'itemcost' : str(float(float(itemprice)*float(itemqty)))})
                    else:
                        messages.warning(request, 'BoQ item quantity and Price must be a decimal number')
                        return redirect('/update_boq/0')
            boq_project.submitted_boq = boq
            boq_project.workflow = str(boq_project.workflow) + ']*[' + 'BoQ updated on ' + str(datetime.now())
            boq_project.save(update_fields=['submitted_boq', 'workflow'])
            notification(boq_project.userid.id, 'BoQ submitted for project: ' + boq_project.name + ' has been updated by PSDF Sectt.' )
            messages.success(request, 'BoQ successfully updated and intimated to user.')
            return redirect('/update_boq/0')
        if projid == '0':
            context['project_list'] = projects.objects.filter(status = '1')
            return render(request, 'psdf_main/_admin_boq.html', context)
        else:
            thisproject = projects.objects.get(id = projid)
            if thisproject:
                context['sub_boq'] = get_boq_details(thisproject.submitted_boq)
                context['proj'] = thisproject
                context['range'] = range(len(context['sub_boq'])+1,1000)
                return render(request, 'psdf_main/_admin_update_boq.html', context)
            return render(request, 'psdf_main/_admin_boq.html', context)
    else:
        return oops(request)
