from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import (
    home_view,
    login_view,
    logout_view,
    forgot_password_view,
    registeration_view,
    check_otp_view,
    check_reset_otp_view,
    reset_new_password_view,
    edit_profile,
    profile_view
    
)

app_name = 'users'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registeration_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('activate-email/', check_otp_view, name='activate_email'),
    path('reset-code/', check_reset_otp_view, name='reset_code'),
    path('new-password/', reset_new_password_view, name='reset_new_password'),
 path('edit-profile/', edit_profile, name='edit_profile'),
 path('profile/', profile_view, name='profile'),
path('get-user-data/', views.get_user_data, name='get_user_data'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
