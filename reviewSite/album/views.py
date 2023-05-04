from django.shortcuts import render
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from album.models import Album
from album.forms import AlbumForm
import os

def movie_info_update(request):
    """
    cron.py에 있는 함수를 호출해 업데이트하고 완료 페이지를 띄웁니다.
    """

    val = "python3 album/cron.py" # cron.py를 사전에 sudo chmod 777로 바꿔주세요
    os.system(val)
    return render(request, 'album/update_after.html')

class IndexView(ListView):
    model = Album
    template_name = 'album/index.html'
    context_object_name = 'albums'
    paginate_by = 10
    ordering = ['id'] # 아이디순으로

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/album_detail.html'
    pk_url_kwarg = 'album_id'

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

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')