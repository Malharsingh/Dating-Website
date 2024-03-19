from django.urls import path, include
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'dating_app'

urlpatterns = [
    path('random_card/', views.random_card, name='random_card'),
    path('<int:user_id>/', views.partner_account, name='partner_account'),

]