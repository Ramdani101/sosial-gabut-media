import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Postingan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploader_name = models.CharField(max_length=150, blank=True)
    uploader_image = models.ImageField(upload_to='post_uploader_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    konten = models.TextField()
    total_share = models.IntegerField(default=0)
    pub_date = models.DateTimeField("date published")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.konten

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        if not self.uploader_name:
            self.uploader_name = self.user.username
        if not self.uploader_image and hasattr(self.user, 'profile'):
            self.uploader_image = self.user.profile.image
        super().save(*args, **kwargs)


class Komentar(models.Model):
    post_id = models.ForeignKey(Postingan, on_delete=models.CASCADE, related_name='comments')
    komentar = models.TextField()
    user_id = models.IntegerField()
    pub_date = models.DateTimeField("date published")
    

    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.komentar


class Suka(models.Model):
    post_id = models.ForeignKey(
        Postingan, on_delete=models.CASCADE, related_name='likes')
    user_id = models.IntegerField()

    class Meta:
        unique_together = ('user_id', 'post_id')
