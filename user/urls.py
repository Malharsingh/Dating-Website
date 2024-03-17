from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [

    path('signup_one/', views.signup_one, name='signup_one'),

]