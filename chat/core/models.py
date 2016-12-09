from django.db import models


class ChatMessage(models.Model):
	room = models.CharField(blank=True, max_length=100)
	message = models.TextField(blank=True)

	time = models.DateField(auto_now_add=True)
	user = models.CharField(blank=True, null=True, max_length=100)