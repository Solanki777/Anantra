from django.urls import path
from . import views

urlpatterns = [
    path(
    "colleges/export/",
    views.export_colleges_excel,
    name="export_colleges_excel",
),

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
    path("college/<int:id>/view/", views.college_view, name="college_view"),
    path("college/<int:id>/edit/", views.edit_college, name="edit_college"),
    path(
    "college/<int:id>/restore/",
    views.restore_college,
    name="restore_college",
    
),
path(
    "college/<int:id>/suspend/",
    views.suspend_college,
    name="suspend_college",
),

    path(
            "action/<str:action>/<int:college_id>/<str:token>/",
            views.email_action,
            name="email_action",
        ),

]