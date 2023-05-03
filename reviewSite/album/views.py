from django.shortcuts import render, redirect
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
    

def comment_create(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(pk=album_id)
        content = request.POST.get('content')
        if content: # 빈 댓글은 생성하지 않음
            Comment.objects.create(
                content=content,
                author=request.user,
                album=album,
            )
    return redirect('album-detail', album_id)

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "선택한 항목이 없습니다."
#         })
#     else:
#         selected_choice.votes = F('votes') + 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))