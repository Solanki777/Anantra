from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from colleges.models import College

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            College.objects.create(
                admin=user,
                college_name=form.cleaned_data["college_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
            )

            messages.success(
                request,
                "College registered successfully."
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

    if request.method=="POST":
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
                "Invalid Username password"
            )
        
    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "you have been logged out successfully."
    )

    return redirect("login")