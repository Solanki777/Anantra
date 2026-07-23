from django.db import models
from django.contrib.auth.models import User


class College(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("suspended", "Suspended"),
    ]

    admin = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="college"
    )

    college_name = models.CharField(max_length=200)

    college_code = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField()
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to="college_logos/",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.college_name