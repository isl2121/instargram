from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from .forms import LoginForm, SignupForm, UpdateForm
from django.contrib import messages
from .models import Profile, Relation
from app.models import App
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

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

@login_required
@require_POST
def set_follow(request):
    print("-*" * 10)
    print(request.POST.get('user'))
    from_user = request.user.profile
    user = request.POST.get('user')
    print("-*-" * 10)

    to_user = get_object_or_404(Profile, user__username=user)

    relation, result = Relation.objects.get_or_create(from_user=from_user, to_user=to_user.user.profile)

    return_data = {}

    if result:
        return_data['result'] = 1
        return_data['msg'] = '팔로우 설정'
    else:
        relation.delete()
        return_data['result'] = 0
        return_data['msg'] = '팔로우 설정이 취소되었습니다.'

    return HttpResponse(json.dumps(return_data), content_type="application/json")



def Update_profile(request):
    pk = request.user.pk
    obj = get_object_or_404(Profile, pk=pk)

    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            profile = form.save()
            messages.info(request,'저장되었습니다.')
        else:
            messages.error(request,'저장중 문제가 발생하였습니다.')

        return HttpResponseRedirect('/user/update_profile')

    else:
        form = UpdateForm(instance=obj)

    return render(request, 'registration/update_profile.html',{'form':form,'profile':obj})


def Update_passwd(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user=user)
            messages.success(request,'패스워드가 변경되었습니다.')
            return HttpResponseRedirect('/user/update_profile')
        else:
            messages.error(request,'패스워드 변경중 실패하였습니다.')
            return HttpResponseRedirect('/user/update_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/update_passwd.html', {'form':form})

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