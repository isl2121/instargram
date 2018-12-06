from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm, SignupForm
from django.contrib import messages

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
# Create your views here.

def login(request):

    if request.user.is_anonymous:

        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():

                id = request.POST['id']
                password = request.POST['password']
                user = authenticate(username=id,password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('app:index')
                else:
                    messages.warning(request, '아이디 / 패스워드를 확인하여주십시요')
                    return HttpResponseRedirect('/account/login')
            else:
                messages.warning('로그인에 문제가 발생하였습니다.')
                return HttpResponseRedirect('account/login')

    form = LoginForm()
    return render(request,'registration/login.html', {'form':form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request,'로그아웃 되셨습니다.')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'registration/login.html')

class SignupUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:signup_done')

class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'

'''
@transaction.atomic
def signup(request):
    if request.method == "POST":

        user_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = User.objects.create_user(**user_form.cleaned_data)
            user.refresh_from_db()

            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.profile.name = profile_form.cleaned_data.get('name')
            user.profile.sex = profile_form.cleaned_data.get('sex')
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')

            user.save()

            auth_login(request, user)

            return redirect('app:index')
        else:
            messages.warning(request, '회원가입중 문제가 발생하였습니다.')
            return HttpResponseRedirect('/account/register')
    else:

        user_form = SignupForm()
        profile_form = ProfileForm()

    return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form':profile_form})
'''