from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Question, QuizAttempt

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'category', 'correct_answer')
    list_filter = ('category',)
    search_fields = ('question_text',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'score', 'timestamp')
    list_filter = ('category', 'timestamp')
    search_fields = ('user__username',)
