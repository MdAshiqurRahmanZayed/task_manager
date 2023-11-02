
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Features/Functionalities
urlpatterns = [
    path("register/",register,name='register'),
    path("login/",login,name='login'),
    path('logout/',logout,name='logout'),
    path("api/token/", MyTokenObtainPairView.as_view(),name='MyTokenObtainPairView'),
    path("token/refresh/", TokenRefreshView.as_view(),name='TokenRefreshView'),
    
    path("dashboard/",dashboard,name="dashboard")
]
