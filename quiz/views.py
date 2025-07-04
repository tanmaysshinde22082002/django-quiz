from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Question, QuizAttempt
from django.utils import timezone
from django.contrib import messages
import random



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard(request):
    categories = Category.objects.all()
    return render(request, 'quiz/dashboard.html', {'categories': categories})



@login_required
def start_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = list(Question.objects.filter(category=category))
    random.shuffle(questions)  # Optional: shuffle questions
    request.session['quiz'] = [q.id for q in questions]
    request.session['score'] = 0
    request.session['current'] = 0
    request.session['category_id'] = category.id
    return redirect('quiz_question')


@login_required
def quiz_question(request):
    quiz = request.session.get('quiz')
    current = request.session.get('current', 0)
    score = request.session.get('score', 0)

    if current >= len(quiz):
        return redirect('quiz_result')

    question_id = quiz[current]
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        selected = request.POST.get('option')
        if selected == question.correct_answer:
            request.session['score'] += 1
        request.session['current'] += 1
        return redirect('quiz_question')

    return render(request, 'quiz/question.html', {'question': question, 'question_number': current + 1, 'total': len(quiz)})



@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    category_id = request.session.get('category_id')
    category = get_object_or_404(Category, id=category_id)
    total_questions = len(request.session.get('quiz', []))

    QuizAttempt.objects.create(
        user=request.user,
        category=category,
        score=score,
        timestamp=timezone.now()
    )


    for key in ['quiz', 'score', 'current', 'category_id']:
        if key in request.session:
            del request.session[key]

    return render(request, 'quiz/result.html', {
        'score': score,
        'total': total_questions,
        'category': category
    })



@login_required
def quiz_history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'quiz/history.html', {'attempts': attempts})
