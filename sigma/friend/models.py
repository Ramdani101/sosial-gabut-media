from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend_username = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    accepted_at = models.DateTimeField("date accepted")

    def __str__(self):
        return self.friend_username.username



