from test_app import views
from django.urls import path, include

urlpatterns = [
    path('pika/', views.test_pika, name='test_pika'),
]