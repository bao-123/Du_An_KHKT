from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("classes", views.view_classes, name="classes"),
    path("teacher/<int:teacher_id>", views.view_teacher, name="view_teacher"),
    path("student/<int:id>", views.view_student, name="view_student"),
    path("class/<int:id>", views.view_class, name="view_class"),
    path("new_student", views.create_student, name="create_student"),
]