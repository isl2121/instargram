from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App, Comment
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['reply']



class AppForm(forms.ModelForm):

    title = forms.CharField(label='제목', )
    photo = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'class' : 'photo'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'post-new-content',
        'rows': 5,
        'cols': 50,
        'placeholder': '140자 까지 등록 가능합니다.\n#태그명 을 통해서 검색 태그를 등록할 수 있습니다. \n예시 : I #love #coding!', }))

    class Meta:
        model = App
        fields = ['title', 'photo', 'content']
