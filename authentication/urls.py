from django.urls import path

from authentication.views import *

urlpatterns = [
    path('check/auth', CheckAuthentication.as_view(), name='check_authentication'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name='sign-up'),
    path('activate/<str:activation_token>', ActivateAccountView.as_view(), name='activate-account'),
    path('profile', ProfileView.as_view(), name='profile')
]
