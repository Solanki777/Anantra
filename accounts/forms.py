import uuid

from django import forms
from django.contrib.auth.models import User

from colleges.models import College


class RegisterForm(forms.ModelForm):
    """
    College registration form.

    No password fields: the principal/administrator does not choose a
    password at signup. The User account is created with
    set_unusable_password(), and a real temporary password is only
    generated + emailed once staff approve the college (see College.status).
    """

    username = forms.CharField(
        max_length=150,
        label="Principal / Administrator Name",
    )
    email = forms.EmailField(required=True)

    college_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15)
    website = forms.URLField(required=False)
    logo = forms.ImageField(required=False)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # No password collected at signup — locked until the college is
        # approved and a temporary password is issued.
        user.set_unusable_password()

        if commit:
            user.save()

            College.objects.create(
                admin=user,
                college_name=self.cleaned_data["college_name"],
                college_code=self._generate_college_code(),
                email=self.cleaned_data["email"],
                phone=self.cleaned_data["phone"],
                website=self.cleaned_data.get("website", ""),
                logo=self.cleaned_data.get("logo"),
                address=self.cleaned_data["address"],
                city=self.cleaned_data["city"],
                state=self.cleaned_data["state"],
                status="pending",
            )

        return user

    @staticmethod
    def _generate_college_code():
        return f"CLG-{uuid.uuid4().hex[:8].upper()}"