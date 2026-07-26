from django.shortcuts import render, get_object_or_404,redirect
from colleges.models import College
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

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

def approve_college(request,id):
    college = get_object_or_404(College,id=id)

    college.status = "approved"
    college.save()

    messages.success(
        request,
        f"{college.college_name} has been approved successfully."
    )
    return redirect("pending_colleges")

def reject_college(request,id):
    college = get_object_or_404(College,id=id)

    college.status = "rejected"
    college.save()

    messages.warning(
        request,
        f"{college.college_name} has been rejected."
    )
    return redirect("pending_colleges")

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from colleges.models import College


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