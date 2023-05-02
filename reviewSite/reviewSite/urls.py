"""
URL configuration for reviewSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from common.views import CustomPasswordChangeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # common.urls에 Main page 담김 (index.html)
    path('', include('common.urls')),
    # allauth
    path(
        'email-confirmation-done/', # 터미널에 뜨는 이메일 인증 링크 타고 들어가면 이메일 인증 완료
        TemplateView.as_view(template_name='account/email_confirmation_done.html'),
        name='account_email_confirmation_done',
    ),
    path(
        'password/change/',
        CustomPasswordChangeView.as_view(),
        name='account_password_change',
    ),
    path('', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)