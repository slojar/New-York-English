from django.contrib.auth.models import User
from django.db import models


STATUS_CHOICES = (
    ("running", "Running"), ("completed", "Completed")
)

TRANSACTION_STATUS_CHOICES = (
    ("pending", "Pending"), ("success", "Success"), ("failed", "Failed")
)

VOCABULARY_STATUS_CHOICES = (
    ("completed", "Completed"), ("not_completed", "Not Completed")
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateTimeField(blank=True, null=True)
    level = models.CharField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=400, blank=True, null=True)
    subscribed = models.BooleanField(default=False)

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
    image = models.ImageField(upload_to="vocabulary-images", blank=True, null=True)
    audio_file = models.FileField(blank=True, null=True, upload_to="audio-files")
    video_file = models.FileField(blank=True, null=True, upload_to="video-files")

    def __str__(self):
        return f"{self.title}: {self.lesson.name}"


class UserVocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="running")

    def __str__(self):
        return self.vocabulary.title


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # plan = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default="pending")
    detail = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.status}"


