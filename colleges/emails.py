from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_college_registration_email(college):

    subject = f"New College Registration - {college.college_name}"

    body = f"""
A new college has registered on EduTrack.

--------------------------------------------

College Name : {college.college_name}
College Code : {college.college_code}

Admin Name   : {college.admin.username}
Username     : {college.admin.username}
Admin Email  : {college.admin.email}

College Email: {college.email}
Phone        : {college.phone}

State        : {college.state}
City         : {college.city}

Current Status : {college.status.title()}

--------------------------------------------

Please review this registration.

EduTrack
"""

    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,

        # Super Admin Email
        to=["anantra.login7@gmail.com"],
    )

    email.send()