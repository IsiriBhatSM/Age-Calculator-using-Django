from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.add_dob, name='add_dob'),
    # path('save_dob/', views.save_dob, name='save_dob'),
    path('test_cases/', views.test_cases, name='test_cases'),
    path('about_us/',views.about_us, name='about_us')
]

