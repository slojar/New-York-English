from django.contrib.auth.models import User
from django.db import models


STATUS_CHOICES = (
    ("running", "Running"), ("completed", "Completed")
)

TRANSACTION_STATUS_CHOICES = (
    ("pending", "Pending"), ("success", "Success"), ("failed", "Failed")
)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateTimeField(blank=True, null=True)
    level = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="course-images", blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="running")

    def __str__(self):
        return f"{self.user.username}: {self.lesson.name}"


class Vocabulary(models.Model):
    title = models.CharField(max_length=50)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    audio_file = models.FileField(blank=True, null=True, upload_to="audio-files")
    video_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default="pending")
    detail = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.status}"


