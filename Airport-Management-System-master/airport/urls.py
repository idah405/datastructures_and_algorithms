"""airport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="handyman/forgot-password.html",
             html_email_template_name="client/emails/password-reset.html",
             subject_template_name="client/emails/password_reset_subject.txt",
         ),
         name="password_reset"),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="handyman/password-reset-done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="handyman/reset-password.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="handyman/password-reset-complete.html"),
         name="password_reset_complete"),

    path('admin/', admin.site.urls),
    
    path('financemanager/', include(('financemanager.urls', 'financemanager'), namespace="financemanager")),
    path('handyman/', include(('handyman.urls', 'handyman'), namespace="handyman")),
    path('manager/', include(('manager.urls', 'manager'), namespace="manager")),
    path('', include(('client.urls', 'client'), namespace="client")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


