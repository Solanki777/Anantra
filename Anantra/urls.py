=
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("students.urls")),
    path("",include("accounts.urls")),
    path("superadmin/",include("superadmin.urls")),

    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="emails/password_reset_email.html",
        subject_template_name="emails/password_reset_subject.txt",
    ),
    name="password_reset",
),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name = "accounts/password_reset_done.html"
        ),
        name = "password_reset_done",
    ),

    path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
    ),
    name="password_reset_confirm",
),

    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name = "accounts/password_reset_complete.html"
        ),
        name = "password_reset_complete"
    ),
    

   


]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
