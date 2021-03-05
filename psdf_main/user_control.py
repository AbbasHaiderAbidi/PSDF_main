from .helpers import *



def newdpr(request):
    form = NewDPR_form()
    if useronline(request) and not adminonline(request):
        user = userDetails(request.session['user'])
        if request.method == 'POST':
            req = request.POST
            print('hello')

            boq = []
            if request.FILES:
                amount = req['amountasked']
                schedle = req['schedule']
                proname = req['proname']
                boq = []
                user = userDetails(request.session['user'])
                context = {'user':user,'form':form, 'n' : range(1000)}
                for i in range(1,1000):
                    if not (req['itemname'+str(i)] == ''):
                        itemqty = req['itemqty'+str(i)]
                        itemprice = req['itemprice'+str(i)]
                        if isfloat(itemqty) and float(itemprice):
                            boq.append({'itemname':req['itemname'+str(i)],'itemno':req['itemno'+str(i)],'itemdesc': req['itemdesc'+str(i)], 'itemqty': itemqty, 'itemprice': itemprice, 'itemcost' : str(float(float(itemprice)*float(itemqty)))})
                        else:
                            messages.warning(request, 'BoQ item quantity and Price must be a decimal number')
                            return render(request, 'psdf_main/newdpr.html', context)
                print(boq)
                
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
                dpr = request.FILES['dpr']
                a1 = request.FILES['a1']
                if 'otherdoc' in request.FILES:
                    otherdoc = request.FILES['otherdoc']
                newdprpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'),os.path.join(request.session['user'],'temp/'+proname+'_'+amount+'_'+schedle))
                if smkdir(newdprpath):
                    
                    dpr_filename = secure_filename("DPR."+dpr.name.split('.')[1])
                    a1_filename = secure_filename("forms."+a1.name.split('.')[1])
                    if 'otherdoc' in request.FILES:
                        otherdoc_filename = secure_filename("otherdocs."+otherdoc.name.split('.')[1])
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
                    
                    context = {'user':user,'form':form, 'n' : range(1000)}
                    messages.success(request, 'DPR for Project : '+ proname +' has been submitted for examination.')
                    return render(request, 'psdf_main/newdpr.html', context)
            else:

                context = {'user':user,'form':form, 'n' : range(1000)}
                messages.warning(request, 'Please upload supporting documents')
                return render(request, 'psdf_main/newdpr.html', context)

        
        context = {'user':user,'form':form, 'n' : range(1000)}
        return render(request, 'psdf_main/newdpr.html', context)
    return oops(request)



def downloadformat(request,thisdoc):
    filelist = {'support':'DPR_Supporting_documents.zip', 'format':'DPR_Forms.zip','sample1':'sample1.zip','sample2':'sample2.zip','sample3':'sample3.zip'}
    if useronline(request) and not adminonline(request):
        formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Formats/'+filelist[thisdoc])
        if os.path.exists(formatpath):
            with open(formatpath,'rb') as fh:
                response = HttpResponse(fh.read(), content_type = "application/adminupload")
                response['Content-Disposition'] = 'inline;filename =' + filelist[thisdoc]
                return response
        return oops(request)
    else:
        return oops(request)


def notificationread(request, userid):
    if useronline(request):
        user = users.objects.get(id = userid)
        user.notification = ''
        user.save(update_fields=['notification'])
        context = {'user':userDetails(request.session['user'])}
        messages.success(request, 'Notifications now marked as read.')
        return redirect('/')
    else:
        return oops(request)

