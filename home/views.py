import os
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

from home.forms import LoginForm, RegistrationForm, AudioForm
from home.models import *
from home.stripe_api import StripeAPI
from home.utils import complete_payment, transcribe_audio

baseUrl = settings.BASE_URL


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

            user_form = form.save()
            # CREATE USER PROFILE
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            phone = form.cleaned_data.get('phone')
            user = authenticate(request, username=email, password=password)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.phone_number = phone
            user_profile.save()
            amount = float(1.0)
            callback_url = f"{baseUrl}/payment-verify"
            stripe_customer_id = ""
            if not user_profile.stripe_customer_id:
                customer = StripeAPI.create_customer(
                    name=user.get_full_name(),
                    email=user.email,
                    phone=phone
                )
                user_profile.stripe_customer_id = customer.get('id')
                user_profile.save()
                stripe_customer_id = customer.get('id')
            description = "Course Payment"

            while True:
                # payment_reference = payment_link = None
                success, response = StripeAPI.create_payment_session(
                    name=user.get_full_name(),
                    amount=amount,
                    return_url=callback_url,
                    customer_id=stripe_customer_id,
                )
                if not success:
                    # raise InvalidRequestException({'detail': response})
                    # DELETE USER
                    User.objects.get(email=email).delete()
                    messages.success(request, 'Error generating payment link, please try later')
                    return redirect('/')
                if not response.get('url'):
                    # DELETE USER
                    User.objects.get(email=email).delete()
                    messages.success(request, 'Error generating payment link, please try later')
                    return redirect('/')

                payment_reference = response.get('payment_intent')
                if not payment_reference:
                    payment_reference = response.get('id')
                payment_link = response.get('url')
                break

            # Create Transaction
            Transaction.objects.create(user=user, amount=amount, detail=description, transaction_id=payment_reference)

            return HttpResponseRedirect(payment_link)

            # messages.success(request, 'Account registered successfully')
            # return redirect('/login')

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
        'transactions': Transaction.objects.filter(user=request.user).order_by("-id")[:20],
        'total_transaction': Transaction.objects.filter(user=request.user),
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


def verify_payment(request):
    reference = request.GET.get("reference")
    success, response = complete_payment(reference)
    if success is False:
        return redirect(reverse('home:homepage'))
    #     return Response({"detail": response}, status=status.HTTP_400_BAD_REQUEST)
    return redirect(reverse('home:dashboard',))



