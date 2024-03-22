from django.contrib.auth.models import User
from .models import Message
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datingapp.models import Favorite


# Create your views here.
class MessagesListView(LoginRequiredMixin, ListView):
    """ Inbox/messages/user list """
    model = Message
    template_name = 'chat_app/messages_list.html'

    # Contextual data to display the latest message
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)  # Getting your primary key
        messages = Message.get_message_list(user)  # Getting all messages between you and another user

        other_users = []  # List of other users

        # Getting another person's name from a message list and adding it to the list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        context['messages_list'] = messages
        context['other_users'] = other_users
        context['user'] = user
        context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')
        return context
