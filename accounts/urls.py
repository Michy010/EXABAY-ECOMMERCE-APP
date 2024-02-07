from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path ('sign_up/', views.sign_up, name='SignUp'),
    path ('login/', views.login_page, name='SignIn'),
    path ('my_center/', views.my_center, name= 'my_center'),
]


