from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'home'

urlpatterns = [
    path('', home_view, name='homepage'),
    # path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
    path('courses', courses_view, name='courses'),
    path('login', login_view, name='login'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('lesson/<int:pk>', lesson_view, name='lesson'),
    path('lesson-detail/<int:pk>', lesson_detail_view, name='lesson-detail'),
    path('register', register_view, name='register'),
    path('logout', userlogout, name='logout'),
    path('upload_audio/<int:pk>', upload_audio, name='upload_audio'),
    path('payment-verify', verify_payment, name='verify_payment'),
    path('unsubscribed', reset_subscription_counter_job, name='reset_subscription'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


