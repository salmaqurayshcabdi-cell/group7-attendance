from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from students import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('students/', views.student_list, name='student_list'),

    path('add-student/', views.add_student, name='add_student'),

    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),

    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

    path('attendance/', views.attendance_list, name='attendance_list'),

    path('reports/', views.reports, name='reports'),

    path('export-attendance/', views.export_attendance, name='export_attendance'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )