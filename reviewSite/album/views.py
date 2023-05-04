from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from album.models import Album, Comment
from album.forms import AlbumForm
from django.core.exceptions import ValidationError

# Create your views here.

class IndexView(ListView):
    model = Album
    template_name = 'album/index.html'
    context_object_name = 'albums'
    paginate_by = 10
    ordering = ['-dt_created'] # 최신순으로



class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/album_detail.html'
    pk_url_kwarg = 'album_id'
    
    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        album = self.get_object()
        vote_type = request.POST.get('vote_type')
        if vote_type == 'like':
            album.update_positive_votes(request.user)
        elif vote_type == 'dislike' :
            album.update_negative_votes(request.user)
        return self.get(request,*args,**kwargs)



class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album-detail', kwargs={'album_id': self.object.id})

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'
    pk_url_kwarg = 'album_id'

    raise_exception = True
    
    def get_success_url(self):
        return reverse('album-detail', kwargs={'album_id': self.object.id})

    def test_func(self, user):
        album = self.get_object()
        return album.author == user

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'album/album_confirm_delete.html'
    pk_url_kwarg = 'album_id'

    raise_exception = True

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        album = self.get_object()
        return album.author == user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.request.GET.get('error_message')
        return context


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')
    

def comment_create(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(pk=album_id)
        content = request.POST.get('content')
        if not content: # 빈 댓글은 생성하지 않음
            error_message = '댓글 내용을 입력해주세요.'
            context = {'error_message': error_message, 'album': album}
            return render(request, 'album/album_detail.html', context)
        Comment.objects.create(
            content=content,
            author=request.user,
            album=album,
        )
    return redirect('album-detail', album_id)
