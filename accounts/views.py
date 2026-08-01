from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from colleges.emails import send_college_registration_email

from django.contrib.auth.models import User
from django.http import HttpResponse
from decouple import config

from django.core.mail import send_mail

def test_email(request):
    try:
        send_mail(
            subject="Test Email",
            message="This is a test email from Render.",
            from_email=None,
            recipient_list=["anantra.login7@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"❌ Error: {repr(e)}")


def create_admin(request):
    username = config("ADMIN_USERNAME")
    email = config("ADMIN_EMAIL")
    password = config("ADMIN_PASSWORD")

    if User.objects.filter(username=username).exists():
        return HttpResponse("✅ Admin already exists.")

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )

    return HttpResponse("✅ Admin created successfully.")

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            print("✅ Form is valid")

            college = form.save()
            print("✅ Form saved")

            send_college_registration_email(college)

            messages.success(
                request,
                "Registration submitted. Your application is under review — "
                "you'll receive an email once your college has been approved."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect("dashboard")

        else:
            messages.error(
                request,
                "Invalid username or password. If your college's "
                "registration is still pending approval, no login "
                "credentials have been issued yet."
            )

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


