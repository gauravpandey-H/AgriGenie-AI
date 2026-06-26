from django.urls import path
from . import views

urlpatterns = [
    path('detect/', views.disease_detect_view, name='disease_detect'),
]
