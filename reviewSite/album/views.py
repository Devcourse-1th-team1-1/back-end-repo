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
from album.models import Album
from album.forms import AlbumForm

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
    
    def post(self, request, *args, **kwargs):
        album = self.get_object()
        album.update_votes()
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

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')
    
