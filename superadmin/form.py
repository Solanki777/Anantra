from django import forms
from colleges.models import College


class CollegeForm(forms.ModelForm):

    class Meta:
        model = College

        fields = [
            "college_name",
            "college_code",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "logo",
        ]