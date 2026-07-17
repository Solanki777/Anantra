from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentForm
from .models import Student
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from django.db.models import Count
import json
from django.db.models.functions import ExtractMonth



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

    department_data = (
        Student.objects.values("department").annotate(total = Count("department"))
    )

    course_data = (
        Student.objects.values("course").annotate(total = Count("department"))
    )

    department_labels = []
    department_counts = []
    course_labels = []
    course_counts = []
    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }



    monthly_data = (
        Student.objects
        .annotate(month=ExtractMonth("admission_date"))
        .values("month")
        .annotate(total = Count("id"))
        .order_by("month")
        
    )
    monthly_labels = []
    monthly_counts = []

    for item in monthly_data:

        monthly_labels.append(
            month_names[item["month"]]
        )

        monthly_counts.append(
            item["total"]
        )

    for items in department_data :
        department_labels.append(items["department"])
        department_counts.append(items["total"])

    for item in course_data :
        course_labels.append(item["course"])
        course_counts.append(item["total"])

    context = {
        "total_students" :total_students ,
        "total_departments" : total_departments ,
        "total_courses" : total_courses ,
        "recent_student" : recent_student ,
        "department_labels" :json.dumps(department_labels),
        "department_counts":json.dumps(department_counts),

        "course_labels" :json.dumps(course_labels),
        "course_counts":json.dumps(course_counts),

        "monthly_labels" :json.dumps(monthly_labels),
        "monthly_counts":json.dumps(monthly_counts),


        "department_data": department_data,


    }
    return render(request , "students/dashboard.html" , context)

@login_required
def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST ,request.FILES)

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
            Q(enrollment_no__icontains=search) |
            Q(email__icontains=search) |
            Q(mobile__icontains=search) |
            Q(course__icontains=search) |
            Q(department__icontains=search) 
        )

    paginator = Paginator(students,5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)



    return render(
        request,
        "students/student_list.html",
        {
            "page_obj" : page_obj,
            "students": students,
        }

                )

@login_required
def edit_student(request, id):
    
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        old_photo = student.photo

        form =StudentForm(request.POST, request.FILES , instance=student)

        if form.is_valid():
            if "photo" is request.FILES and old_photo:
                old_photo.delete(save=False)
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
    student = get_object_or_404(Student, id=id )
    if request.method == "POST":
        if student.photo:
            student.photo.delete(save=False)
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

@login_required
def show_details(request , id):
    student = get_object_or_404(Student, id =id)

    return render(
        request,
        "students/student_details.html",
        {
            "student" : student,
        },
    )


@login_required
def export_student_csv(request):
    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="student.csv"'
    )

    writer =csv.writer(response)

    writer.writerow([
        "ID",
        "Enrollment No",
        "Semester",
        "Name",
        "Email",
        "Mobile",
        "Course",
        "Department",
        "Admission Date",]
    )
    students = Student.objects.all()

    for student in students:
        writer.writerow([
            student.id,
            student.enrollment_no,
            student.get_semester_display(),
            student.name,
            student.email,
            student.mobile,
            student.course,
            student.department,
            student.admission_date.strftime("%d-%m-%Y"),
        ])
    
    return response