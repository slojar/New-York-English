from django.contrib import admin
from .models import *


class VocabularyStackInlineAdmin(admin.StackedInline):
    model = Vocabulary


class LessonModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    search_fields = ['name']
    inlines = [VocabularyStackInlineAdmin]


class UserLessionModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'progress', 'status']
    list_filter = ['status']


class VocabularyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'text']
    search_fields = ['title', 'lesson']


class UserVocabularyModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'vocabulary', 'status']
    list_filter = ['status']


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'transaction_id', 'created_on']
    list_filter = ['status']


admin.site.register(UserProfile)
admin.site.register(Lesson, LessonModelAdmin)
admin.site.register(UserLesson, UserLessionModelAdmin)
admin.site.register(Vocabulary, VocabularyModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)
admin.site.register(UserVocabulary, UserVocabularyModelAdmin)

# Register your models here.
