from django.db import models
from accounts.models import Farmer

class ChatHistory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.farmer.user.username} at {self.timestamp}"
