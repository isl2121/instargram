from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App, Comments
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['reply']
