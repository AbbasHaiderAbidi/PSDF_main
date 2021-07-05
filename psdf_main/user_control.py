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
                                otherdoc_filename = secure_filename("otherdocs."+otherdoc.name.split('.')[1])
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
    filelist = {'support':'DPR_Supporting_documents.zip', 'format':'DPR_Forms.zip','sample1':'sample1.zip','sample2':'sample2.zip','sample3':'sample3.zip'}
    if useronline(request) and not adminonline(request):
        formatpath = os.path.join(os.path.join(BASE_DIR, 'Data_Bank'), 'Admin/Formats/'+filelist[thisdoc])
        # if os.path.exists(formatpath):
        with open(formatpath,'rb') as fh:
            response = HttpResponse(fh.read(), content_type = "application/adminupload")
            response['Content-Disposition'] = 'inline;filename =' + filelist[thisdoc]
            return response
        # return oops(request)
    else:
        return oops(request)


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

