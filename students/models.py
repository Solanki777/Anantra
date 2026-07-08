from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    admission_date = models.DateField()

    def __str__(self):
        return self.name