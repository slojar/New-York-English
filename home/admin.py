from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(Lesson)
admin.site.register(UserLesson)
admin.site.register(Vocabulary)
admin.site.register(Transaction)

# Register your models here.
