from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import App, Comment, Tag
from .forms import CommentForm
import json

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
    queryset = App.objects.all().prefetch_related('comment_set','author__profile__follower_user').select_related('author__profile')
    context_object_name = 'app_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = App.objects.all().prefetch_related('comment_set', 'tag_setting','author__profile__follower_user').select_related('author__profile')
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        return context

class MakeApp(CreateView):
    model = App
    fields = ['title', 'image', 'content']
    template_name = 'app/app_make.html'
    success_url = reverse_lazy('app:index')

    def form_valid(self, form):
        object = form.save(commit=False)
        self.request.POST.get('content')
        object.user = self.request.user
        object.save()

        return super().form_valid(form)

@login_required
@require_POST
def comment_new(request):
    pk = request.POST.get('pk')
    app = get_object_or_404(App, pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.app = app
        comment.save()
        return render(request, 'app/ajax/comment_new_ajax.html', {
            'comment': comment,
        })
    else:
        return_data = {}
        return_data['result'] = 0
        return_data['msg'] = '등록중 오류가발생하였습니다.'

    return HttpResponse(json.dumps(return_data), content_type="application/json")


def get_tag(request):
    pass


@login_required
@require_POST
def comment_del(request):
    pk = request.POST.get('pk')
    reply = get_object_or_404(Comment, pk=pk)
    return_data = {}

    if request.user == reply.user:
        reply.delete()
        return_data['result'] = 1
        return_data['msg'] = '메시지를 삭제하였습니다.'
    else:
        return_data['result'] = 0
        return_data['msg'] = '메시지 삭제중 오류가 발생하였습니다.'

    return HttpResponse(json.dumps(return_data), content_type="application/json")

def like_chage(request):
    pk = request.POST.get('pk')
    user = request.user

    app = get_object_or_404(App, pk=pk)

    return_data = {}

    if user in app.likes.all():
        app.likes.remove(user)
        return_data['msg'] = '좋아요 가 취소 되었습니다.'
        return_data['result'] = 0
    else:
        app.likes.add(user)
        return_data['msg'] = '좋아요'
        return_data['result'] = 1

    return_data['count'] = app.like_count()
    return_data['user'] = request.user.get_username()

    return HttpResponse(json.dumps(return_data), content_type="application/json")
