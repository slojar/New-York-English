import os
import uuid
import requests
import environ

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from home.forms import LoginForm, RegistrationForm, AudioForm
from home.models import *

env = environ.Env()

X_RapidAPI_Key = env('X_RapidAPI_Key', None),
X_RapidAPI_Host = env('X_RapidAPI_Host', None),
RapidAPIUrl = env('RapidAPIUrl', None),


def transcribe_audio(file_path, file_name):
    url = RapidAPIUrl
    payload = {}
    files = [('file', (f'{file_name}', open(f'{file_path}', 'rb'), 'audio/wav'))]
    headers = {
        'X-RapidAPI-Key': X_RapidAPI_Key,
        'X-RapidAPI-Host': X_RapidAPI_Host
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    result = ""
    if response.status_code == 200:
        result = response["text"]

    # response = {
    #     "success": True,
    #     "text": "What is your name"
    # }
    # result = response["text"]
    return result


def home_view(request):
    context = {
        'plans': Lesson.objects.all().order_by('price')[:3],
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
    lesson = UserLesson.objects.get(id=pk)
    user_vocabularies = [{
        "id": item.id,
        "title": item.vocabulary.title,
        "status": item.status,
        "text": item.vocabulary.text,
        "image": item.vocabulary.image,
    } for item in UserVocabulary.objects.filter(vocabulary__lesson=lesson.lesson)]

    context = {
        'profile': profile,
        'lesson': lesson,
        'user_vocabularies': user_vocabularies
    }
    return render(request, 'home/lesson.html', context)


def lesson_detail_view(request, pk):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'volca': UserVocabulary.objects.get(id=pk, user=request.user),
    }
    return render(request, 'home/lesson-detail.html', context)


def upload_audio(request, pk):
    # GET Volcabulary
    volca = UserVocabulary.objects.get(id=pk)
    text = volca.vocabulary.text
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.cleaned_data['audio']
            random_filename = f"{uuid.uuid4()}.wav"
            audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', random_filename)

            # Ensure the media directory exists
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)

            with open(audio_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

                response = transcribe_audio(file_path=audio_path, file_name=random_filename)
                if str(response).lower() != str(text).lower():
                    messages.error(request, f'Words mismatch!!!')
                    messages.error(request, f'Course Text: {text}')
                    messages.error(request, f'Your Response: {response}')
                    return redirect(reverse('home:upload_audio', args=[pk]))
                # Update UserVocabulary to complete
                volca.status = "completed"
                volca.save()
            return redirect(reverse('home:lesson-detail', args=[pk]))
    else:
        form = AudioForm()
    return render(request, 'home/audio.html', {'form': form})


