
from django.urls import path
from .views import get_request_token
from .views import direct_login
from .views import initiate_oauth2
from .views import make_authenticated_api_call
from .import views


app_name = 'payments'
urlpatterns = [
    path('get_request_token/', get_request_token, name='get_request_token'),
    path('direct_login/', direct_login, name='direct_login'),
    path('initiate_oauth2/', initiate_oauth2, name='initiate_oauth2'),
    path('make_authenticated_api_call/', make_authenticated_api_call, name='make_authenticated_api_call'),
]