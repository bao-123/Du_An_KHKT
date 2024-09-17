from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register")
]