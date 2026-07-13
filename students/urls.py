from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home") ,
    path("dashboard/",views.dashboard,name="dashboard"),
    path("add/", views.add_student, name="add_student"),
    path("students/", views.student_list, name="student_list"),
    path(
        "edit/<int:id>/",
        views.edit_student,
        name="edit_student"
    ),
    path(
        "delete/<int:id>/",
        views.delete_student,
        name ="delete_student"
    ),
]