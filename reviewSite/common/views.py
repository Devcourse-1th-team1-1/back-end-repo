from allauth.account.views import PasswordChangeView
from django.urls import reverse
from django.shortcuts import render

def index(request):
    return render(request, 'account/index.html') # 메인 화면

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index') # 비밀번호 변경 후 메인으로 돌아감