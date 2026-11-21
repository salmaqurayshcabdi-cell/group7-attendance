import csv
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse

from .models import Student, Attendance
from .forms import StudentForm


# HOME PAGE
def home(request):
    students = Student.objects.all().order_by('-id')

    return render(request, 'home.html', {
        'students': students
    })


# STUDENT LIST AND SEARCH
def student_list(request):
    query = request.GET.get('search', '')

    students = Student.objects.all().order_by('-id')

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query)
        )

    return render(request, 'home.html', {
        'students': students,
        'search': query
    })


# ADD STUDENT
def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'add_student.html', {
        'form': form
    })


# EDIT STUDENT
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    form = StudentForm(
        request.POST or None,
        request.FILES or None,
        instance=student
    )

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'edit_student.html', {
        'form': form,
        'student': student
    })


# DELETE STUDENT
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()

    return redirect('student_list')


# ATTENDANCE LIST
def attendance_list(request):
    students = Student.objects.all().order_by('full_name')
    today = timezone.localdate()

    if request.method == 'POST':
        attendance_date = request.POST.get('date', str(today))

        for student in students:
            status = request.POST.get(f'status_{student.id}')

            if status in ['Present', 'Absent']:
                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={'status': status}
                )

        return redirect('attendance_list')

    existing_attendance = Attendance.objects.filter(date=today)

    attendance_data = {
        record.student_id: record.status
        for record in existing_attendance
    }

    return render(request, 'attendance.html', {
        'students': students,
        'today': today,
        'attendance_data': attendance_data
    })


# REPORTS
def reports(request):
    total_students = Student.objects.count()

    attendance_records = Attendance.objects.select_related(
        'student'
    ).all().order_by('-date')

    selected_date = request.GET.get('date', '')

    if selected_date:
        try:
            datetime.strptime(selected_date, '%Y-%m-%d')
            attendance_records = attendance_records.filter(
                date=selected_date
            )
        except ValueError:
            selected_date = ''

    total_present = attendance_records.filter(
        status='Present'
    ).count()

    total_absent = attendance_records.filter(
        status='Absent'
    ).count()

    total_attendance = total_present + total_absent

    attendance_percentage = (
        round((total_present / total_attendance) * 100, 2)
        if total_attendance > 0 else 0
    )

    context = {
        'total_students': total_students,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage,
        'selected_date': selected_date,
    }

    return render(request, 'reports.html', context)


# EXPORT ATTENDANCE REPORT TO CSV
def export_attendance(request):
    selected_date = request.GET.get('date', '')

    attendance_records = Attendance.objects.select_related(
        'student'
    ).all().order_by('-date')

    if selected_date:
        try:
            datetime.strptime(selected_date, '%Y-%m-%d')
            attendance_records = attendance_records.filter(
                date=selected_date
            )
        except ValueError:
            selected_date = ''

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="attendance_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Date',
        'Student ID',
        'Full Name',
        'Status'
    ])

    for record in attendance_records:
        writer.writerow([
            record.date,
            record.student.student_id,
            record.student.full_name,
            record.status
        ])

    return response