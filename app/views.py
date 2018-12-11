from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import App, Comment, Tag
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


# Create your views here.
def main(request):
    if request.user.is_authenticated:
        print(request.user.username)
        print('login')
    else:
        print('none')

    return render(request, 'app/index.html')

class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


class MainLv(ListView):
    model = App
    context_object_name = 'app_list'
    paginator_class = SafePaginator
    paginate_by = 5


    def get_queryset(self):

        tag = self.kwargs.pop('tag', '')

        if tag:
            queryset = App.objects.filter(tag_setting__tag__iexact=tag)\
                .prefetch_related('comment_set', 'tag_setting','user__profile__follower_user')\
                .select_related('user__profile').order_by('-created_time')
        elif self.request.path == reverse_lazy('app:follow_user'):
            queryset = App.objects.filter(user__profile__in=self.request.user.profile.get_follower) \
                .prefetch_related('comment_set', 'tag_setting', 'user__profile__follower_user') \
                .select_related('user__profile').order_by('-created_time')
        else:
            queryset = App.objects.all() \
                .prefetch_related('comment_set', 'tag_setting', 'user__profile__follower_user') \
                .select_related('user__profile').order_by('-created_time')

        return queryset





class MakeApp(CreateView):
    model = App
    fields = ['title', 'image', 'content']
    template_name = 'app/app_make.html'
    success_url = reverse_lazy('app:index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()

        return super().form_valid(form)


class Modifyapp(UpdateView):
    model = App
    fields = ['title', 'image', 'content']
    template_name = 'app/app_make.html'
    success_url = reverse_lazy('app:index')

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        user = self.request.user
        return get_object_or_404(App, pk=pk, user=user)

class Deleteapp(DeleteView):
    model = App
    success_url = reverse_lazy('app:index')
    template_name = "app/app_delete.html"
    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        user = self.request.user
        return get_object_or_404(App, pk=pk,user=user)

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

def get_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_profile = user.profile
    user_app = user.app_set.all()

    data = {}
    data['user_info'] = user
    data['user_profile'] = user_profile
    data['apps'] = user_app

    return render(request, 'app/user_list.html', data)
