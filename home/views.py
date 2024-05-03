from django.shortcuts import render


def home_view(request):
    context = {
        # 'plan': Plan.objects.all().order_by('min_amount'),
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
    context = {}
    return render(request, 'home/courses.html', context)


def login_view(request):
    context = {}
    return render(request, 'home/login.html', context)


def register_view(request):
    context = {}
    return render(request, 'home/register.html', context)

