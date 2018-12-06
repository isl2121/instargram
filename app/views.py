from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import App

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        print(request.user.username)
        print('login')
    else:
        print('none')

    return render(request, 'app/index.html')

class MainLv(ListView):
    model = App
    queryset = App.objects.all()

