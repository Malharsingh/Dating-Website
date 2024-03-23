from django.urls import path
from .views import MessagesListView

app_name = 'chatapp'

urlpatterns = [
    path('', MessagesListView.as_view(), name='message_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
]