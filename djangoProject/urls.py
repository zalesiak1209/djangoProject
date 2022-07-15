"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

# Project
from app import views
from app.views import category_show_all_content
from app.views import category_show_content
from app.views import create_ogloszenie
from app.views import delete_ogloszenie
from app.views import log_in_to_continue
from app.views import moje_ogloszenia_show_detail
from app.views import ogloszenie_show_detail
from app.views import profil_edit
from app.views import show_my_ogloszenia
from app.views import show_my_profile

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', TemplateView.as_view(template_name='app/homepage.html'), name='homepage'),

                  path('kategoria/', category_show_content, name="kategory_show"),
                  path('kategoria/<int:kategoria_id>', category_show_all_content, name="category_show_all_content"),
                  path('kategoria/<int:kategoria_id>/<int:ogloszenie_id>', ogloszenie_show_detail,
                       name="ogloszenie_show_detail"),
                  path('create_ogloszenie/', create_ogloszenie, name="create_ogloszenie"),
                  path('login/', auth_views.LoginView.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('home/', views.home, name='home'),
                  path('register/', views.register, name='register'),
                  path('moje_ogloszenia/', show_my_ogloszenia, name="show_my_ogloszenia"),
                  path('moje_ogloszenia/<int:id>', moje_ogloszenia_show_detail, name="moje_ogloszenia_show_detail"),
                  path('delete_ogloszenie/<int:id>', delete_ogloszenie, name='delete_ogloszenie'),
                  path('log_in_to_continue/', log_in_to_continue, name='log_in_to_continue'),
                  path("user_profile/", show_my_profile, name='show_my_profile'),
                  path('user_profile/edit', profil_edit, name='edit_profil'),
                  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
                  path('verify_email/', TemplateView.as_view(template_name='registration/verify_email.html'),
                       name='verify_email'),
                  path('confirmation_sucess/',
                       TemplateView.as_view(template_name='registration/confirmation_email_success.html'),
                       name='confirmation_email_sucess'),
                  path('confirmation_fail/',
                       TemplateView.as_view(template_name='registration/confirmation_email_fail.html'),
                       name='confirmation_email_fail'),
                  path('confirm_registration/',
                       TemplateView.as_view(template_name='registration/confirm_registration.html'),
                       name='confirm_registration'),
                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name="password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
                  path("password_reset", views.password_reset_request, name="password_reset"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
