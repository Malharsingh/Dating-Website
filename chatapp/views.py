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


class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'chat_app/inbox.html'
    queryset = User.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        other_user = User.objects.get(username=self.kwargs.get("username"))
        messages = Message.get_message_list(user)

        other_users = []

        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        sender = other_user
        recipient = user

        context['messages'] = Message.get_all_messages(sender, recipient)
        context['messages_list'] = messages
        context['other_person'] = other_user
        context['user'] = user
        context['other_users'] = other_users
        context['favorites'] = Favorite.objects.filter(user=self.request.user).order_by('-saved_date')

        return context

    def post(self, request, *args, **kwargs):
        # print("sender: ", request.POST.get("user"))
        # print("recipient: ", request.POST.get('recipient'))
        sender = User.objects.get(pk=request.POST.get('user'))
        recipient = User.objects.get(pk=request.POST.get('recipient'))
        message = request.POST.get('message')

        if request.user.is_authenticated:
            if request.method == 'POST':
                if message:
                    Message.objects.create(sender=sender, recipient=recipient, message=message)
            return redirect('chat_app:inbox', username=recipient.username)

        else:
            # return render(request, 'auth/login.html')
            pass
