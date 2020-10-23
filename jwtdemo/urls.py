"""jwtdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from api.views import LoginView, OrderView, JwtLoginView,JwtOrderView,ProLogin,ProOrder
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('api/jwt/login/', JwtLoginView.as_view()),
    path('api/order/', OrderView.as_view()),
    path('api/jwt/order/', JwtOrderView.as_view()),
    path('api/jwtlogin/', ProLogin.as_view()),
    path('api/jwtorder/', ProOrder.as_view())
]
