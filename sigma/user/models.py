from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class User(AbstractUser):
#     class Role(models.TextChoices):
#         ADMIN = 'admin', 'Admin'
#         REGULAR = 'regular', 'Regular User'
#         PREMIUM = 'premium', 'Premium User'
#     role = models.CharField(max_length=10, choices=Role.choices, default=Role.REGULAR)
#     base_role = Role.ADMIN
    
#     def save(self, *args, **kwargs):
#         if not self.role:
#             self.role = self.base_role
#         super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images', default='default.jpg')
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        REGULAR = 'regular', 'Regular User'
        PREMIUM = 'premium', 'Premium User'
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.REGULAR)
    base_role = Role.REGULAR

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.base_role
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # waktu upload

    def total_likes(self):
        return self.like_set.count()

    def total_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return f"{self.user.username}'s post on {self.created_at.date()}"