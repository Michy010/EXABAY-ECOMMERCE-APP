from django.urls import path
from . import views

app_name = 'GetCode'
urlpatterns = [
    path ('', views.index, name='home'),
    path ('user_profile/', views.user_profile, name= 'profile'),
    path ('trade_now/', views.trade_now, name='trade_now'),
]