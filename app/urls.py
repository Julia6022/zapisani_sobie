from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.templatetags.static import static

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),

    path('profile/', views.profile, name='profile'),
    path('profile/profile_settings', views.profile_settings, name='profile_settings'),
    path('profile/account_settings', views.account_settings, name='account_settings'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),

    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/view_message/<int:message_id>/', views.view_message, name='view_message'),
    path('inbox/view_message/<int:message_id>/send_reply', views.send_reply, name='send_reply'),
]
