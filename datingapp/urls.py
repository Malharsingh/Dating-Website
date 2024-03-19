from django.urls import path

from . import views

app_name = 'datingapp'

urlpatterns = [
    path('random_card/', views.random_card, name='random_card'),
    path('<int:user_id>/', views.partner_account, name='partner_account'),

]
