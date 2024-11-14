from django.urls import path
from . import views
from .import api

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("", views.index, name="index"),
    path("about", views.about, name="about_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("teaching_classes", views.view_teaching_classes, name="teaching_classes"),
    path("classes", views.view_classes, name="classes"),
    path("teachers", views.view_teachers, name="view_teachers"),
    path("teacher/<int:teacher_id>", views.view_teacher, name="view_teacher"),
    path("student/<int:id>", views.view_student, name="view_student"),
    path("class/<int:id>", views.view_class, name="view_class"),
    path("parent/<int:id>", views.view_parent, name="view_parent"),
    path("new_student", views.create_student, name="create_student"),
    #* this use for update the form teacher of a particular class
    path("class", views.update_class, name="update_class"),
    #*APIs for getting student info
    path("student/marks/<int:id>", views.get_marks, name="student_mark"),
    path("search_student", views.search_student, name="search_student"),
    #*This API is for create student's profile
    path("new_profile/<int:student_id>", api.create_profile, name="create_profile"),
    #* get marks of whole class
    path("marks/<int:id>", api.get_class_marks, name="class_marks"),
    #-i API for update user data
    path("change_info", views.change_info, name="change_user_info"),
    path("change_password", views.change_password, name="change_password"),
    path("advice", api.get_student_advice, name="get_advice")
]