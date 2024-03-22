from django.urls import path
from .views import MessagesListView

app_name = 'chatapp'

urlpatterns = [
    path('', MessagesListView.as_view(), name='message_list'),
]