from django.shortcuts import render, get_object_or_404,redirect
from colleges.models import College
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate,login ,logout
from django.core.mail import send_mail
from .decorators import superadmin_required
from django.contrib.auth.models import User
import secrets
import string
from .form import CollegeForm


def login_view(request):
   

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username = username,
            password = password
        )

        if user and user.is_superuser:
            login(request,user)
            return redirect("superadmin_dashboard")

        messages.error(request,"Invalid Super Admin Credentilas.")

    return render(request,"login.html")

@superadmin_required
def logout_view(request):
    logout(request)
    return redirect("super_admin_login")


@superadmin_required
def dashboard(request):
   
    
    total_colleges = College.objects.count()

    pending_colleges = College.objects.filter(
        status = "pending"
    ).count()

    approved_colleges = College.objects.filter(
        status = "approved"
    ).count()

    rejected_colleges = College.objects.filter(
        status = "rejected"
    ).count()

    context = {
        "total_colleges": total_colleges,
        "pending_colleges" :   pending_colleges,
        "approved_colleges" : approved_colleges,
        "rejected_colleges" : rejected_colleges,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )

@superadmin_required
def pending_colleges(request):

    colleges = College.objects.filter(
        status="pending").order_by("-created_at")

    context = {
        "colleges" : colleges,
    }

    return render(
        request,
        "pending_colleges.html",
        context,
    )

@superadmin_required
def college_details(request,id):
   
    
    college = get_object_or_404(College,id=id)

    context = {
        "college":college,
    }
    return render(
        request,
        "college_details.html",
        context,
    )




@superadmin_required
def approve_college(request, id):
    college = get_object_or_404(College, id=id)
    user = college.admin

    # Generate a temporary password
    chars = string.ascii_letters + string.digits + "@#$%!"
    password = "".join(secrets.choice(chars) for _ in range(10))

    # Use email as username
    user.username = user.email
    user.set_password(password)
    user.is_active = True
    user.save()

    # Update college status
    college.status = "approved"
    college.save()

    # Send login credentials
    send_mail(
        subject="College Registration Approved",
        message=f"""
Dear {college.college_name},

Congratulations! Your college registration has been approved.

Your login credentials are:

Email: {user.email}
Password: {password}

Please log in and change your password after your first login.

Regards,
InterEdu Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        f"{college.college_name} has been approved successfully. Login credentials have been sent to {user.email}."
    )

    return redirect("pending_colleges")



@superadmin_required
def reject_college(request,id):
    
    college = get_object_or_404(College,id=id)

    college.status = "rejected"
    college.save()

    messages.warning(
        request,
        f"{college.college_name} has been rejected."
    )
    return redirect("pending_colleges")



@superadmin_required
def list_colleges(request, status=None):
   
    colleges = College.objects.all().order_by("-created_at")

    # Filter by status
    if status:
        colleges = colleges.filter(status=status)

    # Single Search
    search = request.GET.get("search", "").strip()

    if search:
        colleges = colleges.filter(
            Q(college_name__icontains=search) |
            Q(college_code__icontains=search) |
            Q(admin__first_name__icontains=search) |
            Q(admin__last_name__icontains=search) |
            Q(admin__username__icontains=search) |
            Q(email__icontains=search) |
            Q(state__icontains=search) |
            Q(city__icontains=search) |
            Q(status__icontains=search)
        ).distinct()

    # Pagination
    paginator = Paginator(colleges, 10)
    page = request.GET.get("page")
    colleges = paginator.get_page(page)

    # Dynamic page title
    titles = {
        None: "All Colleges",
        "pending": "Pending Colleges",
        "approved": "Approved Colleges",
        "rejected": "Rejected Colleges",
        "suspended": "Suspended Colleges",
    }

    context = {
        "page_title": titles.get(status, "All Colleges"),
        "current_status": status if status else "all",

        "colleges": colleges,

        # Keep search value in the input
        "search": search,

        # Dashboard cards
        "total_colleges": College.objects.count(),
        "pending_count": College.objects.filter(status="pending").count(),
        "approved_count": College.objects.filter(status="approved").count(),
        "rejected_count": College.objects.filter(status="rejected").count(),
        "suspended_count": College.objects.filter(status="suspended").count(),

        # Dropdowns (optional if you removed them)
        "state_list": College.objects.values_list(
            "state", flat=True
        ).distinct().order_by("state"),

        "city_list": College.objects.values_list(
            "city", flat=True
        ).distinct().order_by("city"),
    }

    return render(
        request,
        "colleges_list.html",
        context,
    )

@superadmin_required
def college_view(request, id):
    college = get_object_or_404(College, id=id)

    return render(request, "college_view.html", {
        "college": college,
    })

@superadmin_required
def edit_college(request,id):
    college = get_object_or_404(
        College,
        id=id,
        status = "approved"
    )

    if request.method == "POST":
        form = CollegeForm(
            request.POST,
            request.FILES,
            instance = college

        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "College updated successfully."
            )

            return redirect("colleges_lsit")
    else:
        form = CollegeForm(instance=college)

    return render(
        request,
        "edit_college.html",
        {
            "form": form,
            "college": college
        }
    )

    