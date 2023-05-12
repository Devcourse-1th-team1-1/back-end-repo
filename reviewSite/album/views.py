from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
)
from album.models import Album, Comment
from album.forms import AlbumForm
from django.core.exceptions import ValidationError


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
    
    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        album = self.get_object()
        vote_type = request.POST.get('vote_type')
        if vote_type == 'like':
            album.update_positive_votes(request.user)
        elif vote_type == 'dislike' :
            album.update_negative_votes(request.user)
        return self.get(request,*args,**kwargs)


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
