from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from home.forms import LoginForm, RegistrationForm
from home.models import *


def home_view(request):
    context = {
        'plans': Lesson.objects.all().order_by('price')[:3],
        # 'recent_transactions': Transaction.objects.filter(status='success').order_by('-id')[:6],
        # 'users': User.objects.all().count(),
        # 'trans': Transaction.objects.all().count(),
    }
    return render(request, 'home/index.html', context)


def about_view(request):
    context = {}
    return render(request, 'home/about.html', context)


def contact_view(request):
    context = {}
    return render(request, 'home/contact.html', context)


def courses_view(request):
    courses = Lesson.objects.all().order_by("price")
    context = {
        'courses': courses,
    }
    return render(request, 'home/courses.html', context)


def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/dashboard')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                messages.error(request, 'Login details are not correct')
                return redirect(reverse('home:login'))
    context = {
        'form': form,
    }
    return render(request, 'home/login.html', context)


def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('/dashboard')

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            get_email = User.objects.filter(email=form.cleaned_data.get('email'))
            if get_email:
                messages.error(request, 'Email address already registered')
                return redirect(reverse('home:register'))

            user = form.save()
            # Thread(target=send_welcome_email_to_user, args=[user]).start()
            messages.success(request, 'Account registered successfully')
            print(messages)
            return redirect('/login')

    context = {
        'form': form,
    }
    return render(request, 'home/register.html', context)


def userlogout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def dashboard_view(request):
    profile = UserProfile.objects.filter(user=request.user).last()
    # transactions = Transaction.objects.filter(user=request.user).order_by('-id')
    # current_profit = Investment.objects.filter(user=request.user, status='active').aggregate(Sum('current_profit'))['current_profit__sum'] or 0
    # all_deposit = Investment.objects.filter(user=request.user, status='active').aggregate(Sum('amount_invested'))['amount_invested__sum'] or 0

    # update user's balance
    # profile.total_earning = current_profit
    # profile.total_deposit = all_deposit
    # profile.total_balance = float(current_profit) + float(all_deposit)
    # profile.save()

    context = {
        'profile': profile,
        'completed': UserLesson.objects.filter(user=request.user, status="completed"),
        'running': UserLesson.objects.filter(user=request.user, status="running"),
        'transactions': Transaction.objects.filter(user=request.user).order_by("-id")[:20]
    }
    return render(request, 'home/dashboard.html', context)


@login_required(login_url='/login')
def lesson_view(request, pk):
    profile = UserProfile.objects.get(user=request.user)
    # transactions = Transaction.objects.filter(user=request.user).order_by('-id')
    # current_profit = Investment.objects.filter(user=request.user, status='active').aggregate(Sum('current_profit'))['current_profit__sum'] or 0
    # all_deposit = Investment.objects.filter(user=request.user, status='active').aggregate(Sum('amount_invested'))['amount_invested__sum'] or 0

    # update user's balance
    # profile.total_earning = current_profit
    # profile.total_deposit = all_deposit
    # profile.total_balance = float(current_profit) + float(all_deposit)
    # profile.save()

    context = {
        'profile': profile,
        'lesson': UserLesson.objects.get(id=pk),
    }
    return render(request, 'home/lesson.html', context)


def lesson_detail_view(request):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'transactions': "transactions",
    }
    return render(request, 'home/lesson-detail.html', context)

