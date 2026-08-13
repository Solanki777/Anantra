from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
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
    path(
        "show/<int:id>/",
        views.show_details,
        name="show_details"
    ),
    path(
        "export/csv/",
        views.export_student_csv,
        name="export_student_csv",
    ),
    path(
        "import/",
        views.import_students,
        name = "import_students",
    ),
    path(
    "verify/<str:enrollment_no>/",
    views.verify_student,
    name="verify_student",
),
    path(
        "id-card/<int:id>/",
        views.generate_id_card,
        name="generate_id_card",
    ),
    path(
    "id-card/<int:id>/download/",
    views.download_id_card,
    name="download_id_card",
),
path(
    "qr/<int:id>/",
    views.generate_student_qr_view,
    name="generate_student_qr",
),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)