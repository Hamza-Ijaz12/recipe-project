from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    
    context = {}
    return render(request, 'auth_user/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page upon successful registration
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'auth_user/signup.html', context)


def loginpage(request):
    message = ''
    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print('========',username)
        print('========',password)
        try:
            user = User.objects.get(username = username )
            user = authenticate(request,username=username,password=password)
        
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                message = "credentials Invalid"
        except:
            message= 'User does not exists'
            # messages.error(request,"User does not exists")
        
        
    context={'message':message}
    return render(request,'auth_user/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('login')
