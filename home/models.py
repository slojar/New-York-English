from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateTimeField(blank=True, null=True)
    level = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.lesson.name}"


class Vocabulary(models.Model):
    title = models.CharField(max_length=50)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    audio_file = models.FileField(blank=True, null=True, upload_to="audio-files")

    def __str__(self):
        return self.title




