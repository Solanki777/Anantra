from django.shortcuts import render
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
        "collleges" : colleges,
    }

    return render(
        request,
        "superadmin/pending_colleges.html",
        context,
    )
