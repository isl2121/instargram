from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms

class LoginForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    sex_type = (
        ('m', '남자'),
        ('w', '여자')
    )

    name = forms.CharField(max_length=50)
    about = forms.CharField(widget=forms.Textarea())
    sex = forms.ChoiceField(choices = sex_type)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'about', 'sex', 'birth_date']

    def save(self, commit=True):
        print('asdfasdf')
        user = super(SignupForm, self).save(commit=False)
        user.save()

        user.profile.about = self.cleaned_data['about']
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.profile.sex = self.cleaned_data['sex']
        user.profile.name = self.cleaned_data['name']
        user.save()


        return user
