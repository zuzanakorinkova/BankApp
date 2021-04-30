from django.urls import path
from . import views


app_name = 'login_app'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_request/', views.password_reset_request,
         name='password_reset_request'),
    path('request_token/', views.request_token, name="request_token"),
    path('delete_account/', views.delete_account, name='delete_account'),
]
