from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_view, name='predict'),
    path('login/', views.login_view, name='login'),
]