from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]