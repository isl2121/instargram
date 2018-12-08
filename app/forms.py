from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App, Comment
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['reply']
