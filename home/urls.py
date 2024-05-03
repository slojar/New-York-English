from django.urls import path
from .views import *


app_name = 'home'

urlpatterns = [
    path('', home_view, name='homepage'),
    # path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
    path('courses', courses_view, name='courses'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
]


