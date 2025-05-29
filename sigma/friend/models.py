from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Friend(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),  # Opsional, jika Anda ingin mendukung penolakan
    )

    user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    friend_username = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan permintaan
    accepted_at = models.DateTimeField(null=True, blank=True)  # Waktu diterima, boleh null

    def __str__(self):
        return f"{self.user.username} -> {self.friend_username.username} ({self.status})"

    class Meta:
        # Pastikan tidak ada duplikasi permintaan pertemanan
        unique_together = ('user', 'friend_username')

