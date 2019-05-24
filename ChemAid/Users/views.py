from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import View, CreateView

from .forms import ( UserRegisterForm, UserLoginForm, UserUpdateForm, 
    ProfileUpdateForm, adminupdateform, AdminDetailsForm)
from .models import User,Notification
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
# Create your views here.
def home(request):
    user_b = request.user
    notif = Notification.objects.all()
    return render(request,"home.html",{"user_b":user_b,"notif":notif})

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('log_in')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def profile(request):
    user =  request.user
    return render(request, 'profile.html',{'user': user})

def admin(request):
    return render(request, 'admin.html')

@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'updateProfile.html', context)

def log_in(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user.is_admin:
            if next:
                return redirect(next)
            return redirect('adminhome')
        else:
            login(request, user)
            if next:
                return redirect(next)
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'login.html', context)

# Create your views here.
def log_out(request):
	return render(request, 'logout.html')

def adminprofile(request):
        return render(request, 'adminprofile.html')

def adminhome(request):

        return render(request, 'adHome.html')


def updateAdmin(request):
    if request.method == 'POST':
        u_form = adminupdateform(request.POST, instance=request.user)
        p_form = adminprofileupdateform(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user = p_form.save()
          #  login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      
           # messages.success(request, f'Your account has been updated!')
            return redirect('adminprofile')
    else:
        u_form = adminupdateform(instance=request.user)
        p_form = adminprofileupdateform(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'adminprofile.html', context)


def adminlogout(request):
    return render(request, 'adminlogout.html')

def admindetails(request):
    if request.method == 'POST':
        user_form = AdminDetailsForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            #.set_password(user.password)
            user.save()
            #email = form.cleaned_data.get('email')
           #
            return redirect('adminhome')
    else:
        form = AdminDetailsForm()
    return render(request, 'admindetails.html', {'form': form})

def credentials(request):
    return render(request, 'credentials.html')