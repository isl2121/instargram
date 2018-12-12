from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django import forms
import datetime

class LoginForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput, label='아이디')
    password = forms.CharField(widget=forms.PasswordInput, label='패스워드')

class SignupForm(UserCreationForm):
    sex_type = (
        ('m', '남자'),
        ('w', '여자')
    )

    name = forms.CharField(max_length=50,label='이름')
    about = forms.CharField(label='자기소개',widget=forms.Textarea)
    profil_img = forms.ImageField(label='프로필 사진', required=False)
    sex = forms.ChoiceField(choices=sex_type, label='성별')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datetime-input', 'placeholder': 'Select a date'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'profil_img', 'about', 'sex', 'birth_date']


    def clean_profil_img(self):
        profil_img = self.cleaned_data.get('profil_img')
        if not profil_img:
            profil_img = None
        return profil_img

    def save(self, commit=True):

        user = super(SignupForm, self).save(commit=False)
        user.save()
        user.profile.about = self.cleaned_data['about']
        user.profile.profil_img = self.cleaned_data['profil_img']
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.profile.sex = self.cleaned_data['sex']
        user.profile.name = self.cleaned_data['name']
        user.save()

        return user

class UpdateForm(forms.ModelForm):
    about = forms.CharField(label='자기소개', required=False, widget=forms.Textarea(attrs={
        'rows': 4,
        'cols': 50,
        'placeholder': '소개는 150자 까지 등록 가능합니다', }))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datetime-input', 'placeholder': 'Select a date'}))

    class Meta:
        model = Profile
        fields = ['about','name','sex','profil_img','birth_date']

    def __init__(self, *args, **kwargs):
       form = super(forms.ModelForm, self).__init__(*args,**kwargs)
       return form


