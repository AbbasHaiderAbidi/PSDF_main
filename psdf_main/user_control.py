from .helpers import *



def newdpr(request):
    form = NewDPR_form()
    if useronline(request) and not adminonline(request):
        user = userDetails(request.session['user'])
        if request.method == 'POST':
            print('hello')

            if request.FILES:

                amount = request.POST['amountasked']
                schedle = request.POST['schedule']
                proname = request.POST['proname']
                user = userDetails(request.session['user'])
                if not ('dpr' in request.FILES and 'otherdoc' in request.FILES):
                    context = {'user':user,'form':form}
                    messages.warning(request, 'Please select files to upload')
                    return render(request, 'psdf_main/newdpr.html', context)
                if(not isfloat(amount)):
                    context = {'user':user,'form':form}
                    messages.warning(request, 'Amount should be a decimal number')
                    return render(request, 'psdf_main/newdpr.html', context)
                if(not isnum(schedle)):
                    context = {'user':user,'form':form}
                    messages.warning(request, 'Schedule should be a number')
                    return render(request, 'psdf_main/newdpr.html', context)
                if len(proname) < 3:
                    context = {'user':user,'form':form}
                    messages.warning(request, 'Enter a valid project name')
                    return render(request, 'psdf_main/newdpr.html', context)
                dpr = request.FILES['dpr']
                otherdoc = request.FILES['otherdoc']
                newdprpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'),os.path.join(request.session['user'],'temp/'+proname+'_'+amount+'_'+schedle))
                if smkdir(newdprpath):
                    
                    dpr_filename = secure_filename(dpr.name)
                    otherdoc_filename = secure_filename(otherdoc.name)
                    handle_uploaded_file(os.path.join(newdprpath,dpr_filename),dpr)
                    handle_uploaded_file(os.path.join(newdprpath,otherdoc_filename),otherdoc)

                    temp_project = temp_projects()
                    temp_project.proname = proname
                    temp_project.amountasked = amount
                    temp_project.projectpath = newdprpath
                    temp_project.schedule = schedle
                    temp_project.userid = users.objects.get(id = userDetails(request.session['user'])['id'])
                    temp_project.save()
                    
                    context = {'user':user,'form':form}
                    messages.success(request, 'DPR for Project : '+ proname +' has been submitted for examination.')
                    return render(request, 'psdf_main/newdpr.html', context)
            else:

                context = {'user':user,'form':form}
                messages.warning(request, 'Please upload supporting documents')
                return render(request, 'psdf_main/newdpr.html', context)

        
        context = {'user':user,'form':form}
        return render(request, 'psdf_main/newdpr.html', context)
    return oops(request)



def downloadformat(request):
    if useronline(request) and not adminonline(request):
        formatpath = os.path.join(os.path.join(BASE_DIR, 'Data Bank'), 'Formats/DPR_Forms.zip')
        if os.path.exists(formatpath):
            with open(formatpath,'rb') as fh:
                response = HttpResponse(fh.read(), content_type = "application/adminupload")
                response['Content-Disposition'] = 'inline;filename =' + 'DPR_Forms.zip'
                return response
        return oops(request)
    else:
        return oops(request)
