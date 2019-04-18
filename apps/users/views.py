from django.shortcuts import render, render_to_response, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from .models import UserProfile
from django.contrib.auth.hashers import make_password


# from django.contrib.auth import get_user_model
# User = get_user_model()

def page_not_found(request):
    return render_to_response('404.html', status=404)


def bad_request(request):
    return render_to_response('500.html', status=500)


def login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        login_form = UserLoginForm()
    return render(request, 'users/login.html', {
        'login_form': login_form
    })


def logout(request):
    auth.logout(request)
    return render_to_response('happy_recite_word/home.html')


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        print(register_form.is_valid())
        if register_form.is_valid():
            user_password = register_form.cleaned_data['password']
            user_username = register_form.cleaned_data['username']
            user_nickname = register_form.cleaned_data['nickname']
            a = UserProfile.objects.update_or_create(
                username=user_username,
                password=make_password(user_password),
                nickname=user_nickname
            )
            if a:
                user = auth.authenticate(username=user_username, password=user_password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('home'))
    else:
        register_form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'register_form': register_form
    })


def user_info(request):
    return render_to_response('500.html', status=500)
