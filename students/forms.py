from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'full_name',
            'student_id',
            'email',
            'phone',
            'class_name',
            'student_image',
        ]