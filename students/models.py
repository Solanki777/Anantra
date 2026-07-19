from django.db import models
from colleges.models import College

sem_choice = [
    (1, "Semester 1"),
    (2, "Semester 2"),
    (3, "Semester 3"),
    (4, "Semester 4"),
    (5, "Semester 5"),
    (6, "Semester 6"),
    (7, "Semester 7"),
    (8, "Semester 8"),
]
class Student(models.Model):

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="students"

    )
    name = models.CharField(max_length=100)
    enrollment_no = models.CharField(max_length=20 , unique=True,blank=True,null =True)
    semester = models.PositiveSmallIntegerField(
        choices=sem_choice
    )
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    admission_date = models.DateField()
    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null = True
    )
    

    def __str__(self):
        return self.name
    