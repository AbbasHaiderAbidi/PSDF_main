from .helpers import *



def newdpr(request):
    # form = NewDPR_form()
    if useronline(request) and not adminonline(request):
        
        user = userDetails(request.session['user'])
        if(user['temp_boq'] == ''):
            rboq = range(1,0)
            nboq = 1
            n = range(1,1000)
        else:
            rboq = range(1,len(user['temp_boq']['boq'])+1)
            nboq = len(user['temp_boq']['boq'])+1
            n = range(len(user['temp_boq']['boq'])+1,1000)
        context = {'user':user, 'n' : n, 'nboq' : nboq, 'rboq' : rboq}
        if request.method == 'POST':
            req = request.POST
            if req['subtype'] == 'submit':
                boq = []
                if request.FILES:
                    amount = req['amount']
                    schedle = req['schedule']
                    proname = req['proname']
                    boq = []
                    totcost = 0
                    for i in range(1,1000):
                        if not (req['itemname'+str(i)] == ''):
                            itemqty = req['itemqty'+str(i)]
                            itemprice = req['itemprice'+str(i)]
                            if isfloat(itemqty) and float(itemprice):
                                boq.append({'itemname':req['itemname'+str(i)],'itemno':req['itemno'+str(i)],'itemdesc': req['itemdesc'+str(i)], 'itemqty': itemqty, 'itemprice': itemprice, 'itemcost' : str(float(float(itemprice)*float(itemqty)))})
                            else:
                                messages.warning(request, 'BoQ item quantity and Price must be a decimal number')
                                return render(request, 'psdf_main/newdpr.html', context)
                    for k in boq:
                        totcost = totcost + float(k['itemcost'])
                    if not totcost == float(amount):
                        messages.warning(request, 'Total cost of BoQ must be equal to amount entered.')
                        return render(request, 'psdf_main/newdpr.html', context)
                    if not ('dpr' in request.FILES and 'a1' in request.FILES):
                        messages.warning(request, 'Please select files to upload')
                        return render(request, 'psdf_main/newdpr.html', context)

                    if(not isfloat(amount)):
                        messages.warning(request, 'Amount should be a decimal number')
                        return render(request, 'psdf_main/newdpr.html', context)

                    if(not isnum(schedle)):
                        messages.warning(request, 'Schedule should be a number')
                        return render(request, 'psdf_main/newdpr.html', context)

                    if len(proname) < 3:
                        messages.warning(request, 'Enter a valid project name')
                        return render(request, 'psdf_main/newdpr.html', context)
                    ## CHECK FOR AMOUNT EQUALITY
                    dpr = request.FILES['dpr']
                    a1 = request.FILES['a1']
                    if 'otherdoc' in request.FILES:
                        otherdoc = request.FILES['otherdoc']
                    newdprpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'),os.path.join(request.session['user'],'temp/'+proname+'_'+amount+'_'+schedle))
                    if smkdir(newdprpath):
                        try:
                            dpr_filename = secure_filename("DPR."+dpr.name.split('.')[1])
                            a1_filename = secure_filename("forms."+a1.name.split('.')[1])
                            if 'otherdoc' in request.FILES:
                                try:
                                    otherdoc_filename = secure_filename("otherdocs."+otherdoc.name.split('.')[1])
                                except:
                                    otherdoc_filename = secure_filename("otherdocs")
                        except:
                            dpr_filename = secure_filename("DPR")
                            a1_filename = secure_filename("forms")
                            if 'otherdoc' in request.FILES:
                                otherdoc_filename = secure_filename("otherdocs")
                        handle_uploaded_file(os.path.join(newdprpath,dpr_filename),dpr)
                        handle_uploaded_file(os.path.join(newdprpath,a1_filename),a1)
                        if 'otherdoc' in request.FILES:
                            handle_uploaded_file(os.path.join(newdprpath,otherdoc_filename),otherdoc)
                        temp_project = temp_projects()
                        temp_project.proname = proname
                        temp_project.amountasked = amount
                        temp_project.projectpath = newdprpath
                        temp_project.schedule = schedle
                        temp_project.submitted_boq = boq
                        temp_project.userid = users.objects.get(id = userDetails(request.session['user'])['id'])
                        temp_project.save()
                        temp_dpr = users.objects.get(id = user['id'])
                        temp_dpr.tpd = ''
                        temp_dpr.save(update_fields=['tpd'])
                        admin_user = users.objects.get(id = getadmin_id())
                        admin_user.notification = str(admin_user.notification) + ']*[' + 'New project : '+ proname +' has been submitted by user: ' + str(temp_project.userid.username)
                        admin_user.save(update_fields=['notification'])
                        messages.success(request, 'DPR for Project : '+ proname +' has been submitted for examination.')
                        return render(request, 'psdf_main/newdpr.html', context)

                else:

                    messages.warning(request, 'Please upload supporting documents')
                    return render(request, 'psdf_main/newdpr.html', context)
            elif req['subtype'] == 'save':
                amount = req['amount']
                schedle = req['schedule']
                proname = req['proname']
                boq = []
                x = 0
                for i in range(1,1000):
                    if not (req['itemname'+str(i)] == ''):
                        itemqty = req['itemqty'+str(i)]
                        itemprice = req['itemprice'+str(i)]
                        if isfloat(itemqty) and float(itemprice):
                            x = x + 1
                            boq.append({'srno':x, 'itemname':req['itemname'+str(i)],'itemno':req['itemno'+str(i)],'itemdesc': req['itemdesc'+str(i)], 'itemqty': itemqty, 'itemprice': itemprice, 'itemcost' : str(float(float(itemprice)*float(itemqty)))})
                        else:
                            messages.warning(request, 'BoQ item quantity and Price must be a decimal number')
                            return render(request, 'psdf_main/newdpr.html', context)
                saveddpr = {}
                saveddpr['amountasked'] = amount
                saveddpr['schedule'] = schedle
                saveddpr['proname'] = proname
                saveddpr['boq'] = boq
                temp_dpr = users.objects.get(id = user['id'])
                temp_dpr.tpd = saveddpr
                temp_dpr.save(update_fields=['tpd'])
                
            elif req['subtype'] == 'clear':
                temp_dpr = users.objects.get(id = user['id'])
                temp_dpr.tpd = ''
                temp_dpr.save(update_fields=['tpd'])

        return render(request, 'psdf_main/newdpr.html', context)
    return oops(request)



def downloadformat(request,thisdoc):
    filelist = {'support':'DPR_Supporting_documents', 'format':'DPR_Forms','sample1':'sample1','sample2':'sample2','sample3':'sample3'}
    # try:
    if useronline(request) and not adminonline(request):
        formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), os.path.join('Admin/Formats/',filelist[thisdoc]))
        formatpath = glob.glob(formatpath+'*')[0]
        print(formatpath)
        return handle_download_file(formatpath, request)
    else:
        return oops(request)
    # except:
    #     messages.error(request, 'Function unavailable.')
    #     return redirect('/newdpr')


def notificationread(request, userid):
    user = users.objects.get(id = userid)
    if str(user.username) == request.session['user']:
        if useronline(request):
            user.notification = ''
            user.save(update_fields=['notification'])
            
            messages.success(request, 'Notifications now marked as read.')
            return redirect('/')
            context  = full_user_context(request)
            return render(request, 'psdf_main/dashboard.html', context)
    else:
        return oops(request)

def user_boq_view(request, projid):
    if useronline(request):
        splits = projid.split('_')
        projid = splits[0]
        backpage = splits[1]
        if backpage == 'underexamination':
            proj = temp_projects.objects.get(id = projid)
        else:
            proj = projects.objects.get(id = projid)
        backpages = {'underexamination' : 'under_examination', 'usermonitoringprojects':'user_monitoring_projects','userappraisalprojects':'user_appraisal_projects','usertesgprojects':'user_tesg'}
        if proj.userid.username == request.session['user']:
            
            context = full_user_context(request)
            if backpage == 'underexamination':
                project = temp_projectDetails(proj.id)
            else:
                project = projectDetails(proj.id)
            context['proj'] = project
            context['backpage'] = backpages[backpage]
            return render(request, 'psdf_main/_user_view_boq.html', context)
    else:
        return oops(request)
    
def user_back(request, backpage):
    if useronline(request):
        return redirect('/'+backpage)
    else:
        return oops(request)
    
def user_view_all_projs(request):
    if useronline(request):
        context = full_user_context(request)
        userid = context['user']['id']
        userobj = users.objects.get(id = userid)
        context['all_projs'] = projects.objects.filter(deny = False, userid = userobj)
        context['all_rprojs'] = projects.objects.filter(deny = True, userid = userobj)
        context['all_rpprojs'] = temp_projects.objects.filter(deny = True, userid = userobj)
        context['all_temps'] = temp_projects.objects.filter(userid = userobj)
        context['npending'] = temp_projects.objects.filter(deny = False, userid = userobj).count()
        context['ntesg'] = projects.objects.filter(status = '1', deny = False, userid = userobj).count()
        context['nappr'] = projects.objects.filter(status = '2', deny = False, userid = userobj).count()
        context['nmoni'] = projects.objects.filter(status = '3', deny = False, userid = userobj).count()
        context['nfinal'] = projects.objects.filter(status = '4', deny = False, userid = userobj).count()
        context['nreject'] = projects.objects.filter(deny = True, userid = userobj).count() + temp_projects.objects.filter(deny = True, userid = userobj).count()
        
        return render(request, 'psdf_main/_user_view_all_projects.html', context)
    else:
        return oops(request)