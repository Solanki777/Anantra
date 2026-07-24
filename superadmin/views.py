from django.shortcuts import render, get_object_or_404,redirect
from colleges.models import College
from django.contrib import messages

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
