from django.contrib.auth.models import User
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    saved = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    saved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} | Saved {self.saved}'
