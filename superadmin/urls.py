from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("", views.login_view, name="super_admin_login"),
    path("logout/", views.logout_view, name="super_admin_logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="superadmin_dashboard"),

    # College Management
    path("pending/", views.pending_colleges, name="pending_colleges"),
    path("colleges/", views.list_colleges, name="colleges_list"),
    path("colleges/<str:status>/", views.list_colleges, name="colleges_list_status"),
    path("college/<int:id>/", views.college_details, name="college_details"),

    # Actions
    path("college/<int:id>/approve/", views.approve_college, name="approve_college"),
    path("college/<int:id>/reject/", views.reject_college, name="reject_college"),
]