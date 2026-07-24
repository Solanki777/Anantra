from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="superadmin_dashboard"),
    path("pending_colleges/", views.pending_colleges, name="pending_colleges"),
    path(
    "college/<int:id>/",
    views.college_details,
    name = "college_details"),
    path(
        "approve/<int:id>",
        views.approve_college,
        name="approve_college",
    ),

    path(
    "reject/<int:id>/",
    views.reject_college,
    name="reject_college",
    )

]