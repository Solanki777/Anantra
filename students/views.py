from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentForm
from .models import Student
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request,"home.html")

@login_required
def dashboard(request):
    return render(request , "students/dashboard.html")

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
    students = Student.objects.all()

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