from django.db import models

# Create your models here.


class Chat(models.Model):

	name = models.CharField(max_length=16)


class Message(models.Model):

	user = models.ForeignKey(to='user_module.User', on_delete=models.CASCADE)
	chat = models.ForeignKey(to='Chat', on_delete=models.CASCADE)
	message = models.CharField(max_length=128)
	create_time = models.DateTimeField(auto_now_add=True)

