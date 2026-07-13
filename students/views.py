from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentForm
from .models import Student
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,"home.html")

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_departments = (
        Student.objects.values("department")
        .distinct()
        .count()
    )

    total_courses = (
        Student.objects.values("course")
        .distinct()
        .count()
    )
    recent_student =(
        Student.objects.order_by("-id")[:5]
    )
    context = {
        "total_students" :total_students ,
        "total_departments" : total_departments ,
        "total_courses" : total_courses ,
        "recent_student" : recent_student ,

    }
    return render(request , "students/dashboard.html" , context)

@login_required
def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student added successfully."
            )
            return redirect("student_list")
    else:
        form = StudentForm()
        return render(
            request,
            "students/add_student.html",
            {
                "form":form
            }
        )

@login_required
def student_list(request):

    search = request.GET.get("search" , "")

    students = Student.objects.all()

    if search :
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(mobile__icontains=search) |
            Q(course__icontains=search) |
            Q(department__icontains=search) 
        )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students
        }

                )

@login_required
def edit_student(request, id):
    
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        form =StudentForm(request.POST , instance=student)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student Updated Successfully."
            )

            return redirect("student_list")
    
    else:
        form = StudentForm(instance=student)
    
    return render(
        request,
        "students/add_student.html",
        {
            "form":form,
            "student" : student,
        },
    )

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()

        messages.success(
            request,
            "Student deleted successfully")
        
        return redirect("student_list")
    
    return render(
        request,
        "students/delete_studente.html",
        {
            "student" : student
        }
    )