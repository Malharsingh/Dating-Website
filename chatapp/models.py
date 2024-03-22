from django.db import models
from django.contrib.auth.models import User


# The Message model is used to store messages between users
# The sender and recipient fields are foreign keys to the User model

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from: {self.sender} к {self.recipient}'

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    # The function receives all messages between "two" users (requires your pk and the other user's pk)
    def get_all_messages(id_1, id_2):
        messages = []
        # Get messages between two users, sorts them by date (reverse) and adds them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by(
            '-date')  # Receive messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])

        # Receive messages from recipient to sender
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
        for x in range(len(message2)):
            messages.append(message2[x])

        # Since the function is called when viewing the chat, we will return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

    # The function gets all messages between "any" two users (requires your pk)
    def get_message_list(u):
        # Receive all messages
        m = []  # Saves all messages sorted by "latest - first"
        j = []  # Retains all usernames from posts above after removing duplicates
        k = []  # Saves the last message from the usernames sorted above
        for message in Message.objects.all():
            for_you = message.recipient == u  # Messages received by the user
            from_you = message.sender == u  # Messages sent by user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # Sort messages by sender
                m.sort(key=lambda x: x.date, reverse=True)  # Sort messages by date

        """ remove duplicate usernames and get one message (last message)
        to the username (of another user) (between you and the other user) """
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k
