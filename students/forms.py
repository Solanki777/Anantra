from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=[
            "name",
            "enrollment_no",
            "semester",
            "email",
            "mobile",
            "course",
            "department",
            "admission_date",
            "photo"
        ]

        widgets = {
            "semester": forms.Select(
                attrs={"class": "form-select"}
            ),
            "admission_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }