from django.db import models
from django.utils import timezone

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    class_name = models.CharField(max_length=50)
    student_image = models.ImageField(
    upload_to='student_images/',
    blank=True,
    null=True
)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"