from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class College(models.Model):
    admin = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name = "college"
    )

    college_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.CharField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)