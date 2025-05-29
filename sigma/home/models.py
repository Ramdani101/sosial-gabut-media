import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Postingan(models.Model):
    konten = models.TextField()
    total_share = models.IntegerField(default=0)
    pub_date = models.DateTimeField("date published")
    user_id = models.IntegerField()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.konten

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


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
