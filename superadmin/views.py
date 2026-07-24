from django.shortcuts import render, get_object_or_404
from colleges.models import College

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
