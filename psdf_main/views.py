from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .forms import UserForm
from django.contrib import messages
from .models import *
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

# Create your views here.


def online(request):
    if request.session.has_key('user'):
        return True
    else:
        return False

def adminonline(request):
    if online(request) and request.session.has_key('admin'):
        return True
    else:
        return False

def userDetails(username):
    user = {}
    userobj = users.objects.filter(username = username)[:1]
    for user1 in userobj:
        user['username'] = user1.username
        user['nodal'] = user1.nodal
        user['contact'] = user1.contact
        user['address'] = user1.address
        user['utilname'] = user1.utilname
        user['region'] = user1.region
        user['lastlogin'] = user1.lastlogin
        user['reqdate'] = user1.reqdate
        user['aprdate'] = user1.aprdate
        user['admin'] = user1.admin
        user['active'] = user1.active
    return user
    
def loginPage(request):
    
    if online(request):
        user_m = userDetails(request.session['user'])
        return render(request, 'psdf_main/dashboard.html', {'user':user_m})
    
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            context = {}
            user = users.objects.filter(username = username)[:1]


            if not user:
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request, 'psdf_main/login.html')

            for item in user:
                r_username = item.username

            if not user.values('active')[0]['active']:
                if check_password(password,user.values('password')[0]['password']):
                    user_m = userDetails(r_username)
                    request.session['user'] = user_m['username']
                    if user_m['admin']:
                        request.session['admin'] = "admin"
                    return render(request, 'psdf_main/dashboard.html', {'user':user_m})
                else:
                    messages.error(request, 'Invalid username or password. Please try again.')
                    return render(request, 'psdf_main/login.html')
            else:
                messages.error(request, 'User ' + username + ' is currently inactive. Please contact administrator.')
                return render(request, 'psdf_main/login.html')
    return render(request, 'psdf_main/login.html')

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        cnfpassword = request.POST['cnfpassword']
        password = request.POST['password']
        if(password != cnfpassword):
            form.add_error("password" ,"Both password fields must match")
        else:
            if form.is_valid():
                
                form_main = form.save(commit=False)
                form_main.password = make_password(password)
                form_main.save()
                username = form.cleaned_data['username']
                messages.warning(request, 'User : ' +username + ' pending for verification. ')
                return redirect('/')
    context ={'form':form}
    print(form.errors)
    return render(request, 'psdf_main/userRegister.html', context)

def logout(request):

    if online(request):
        user = users.objects.get(username = request.session['user'])
        user.lastlogin = datetime.now()
        user.save(update_fields=['lastlogin'])
        if adminonline(request):
            del request.session['admin']
        del request.session['user']
    return redirect('/')



def newdpr(request):
    if online(request) and not adminonline(request):
        user = userDetails(request.session['user'])
        context = {'user':user}
        return render(request, 'psdf_main/newdpr.html', context)