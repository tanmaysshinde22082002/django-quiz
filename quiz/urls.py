from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # homepage
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/<int:category_id>/', views.start_quiz, name='start_quiz'),
    path('quiz/question/', views.quiz_question, name='quiz_question'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),
    path('history/', views.quiz_history, name='quiz_history'),
]
