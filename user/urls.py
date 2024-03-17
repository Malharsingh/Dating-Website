from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('signup_one/', views.signup_one, name='signup_one'),
    path('user_account/', views.user_account, name='user_account'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/step_three/', views.sign_up_step_three, name='sign_up_step_three'),
    path('signup/step_two/', views.sign_up_step_two, name='sign_up_step_two'),
]
