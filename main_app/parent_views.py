import json
import math
from datetime import datetime
import re
from django.db.models import Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .forms import *
from .models import *
from django.db.models import Avg  # Import Avg
from reportlab.pdfgen    import canvas
from reportlab.lib.utils import ImageReader
from datetime            import datetime
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
import math
from reportlab.lib import colors
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

from django.conf import settings
import os

# @login_required(login_url='login_page')
# def parent_home(request):
#     """
#     Parent home page dashboard.
#     """
#     if request.user.user_type != '6':
#         return redirect('login_page')
    
#     # Get the parent object for the logged-in user
#     parent = Parent.objects.filter(admin=request.user)
#     print("Admin User:", request.user)
#     # Get all students related to this parent
#     students = []
#     if parent:
#         # students = parent.students.all()
#          students = Student.objects.filter(parent=parent)
#          print('rrrr',students)
#     context = {
#         'user': request.user,
#         'page_title': 'Parent Dashboard',
#         'students': students,
#         'total_students': len(students)
#     }
#     return render(request, 'Parent_template/parent_home.html', context)



def parent_home(request):
    if request.user.user_type != '6':
        return redirect('login_page')

    # ✅ Get single Parent object
    parent = Parent.objects.filter(admin=request.user).first()

    students = []
    notifications = []

    if parent:
        # ✅ Correct ForeignKey filtering
        students = Student.objects.filter(parents=parent).select_related('admin', 'course', 'session')
        notifications = ParentAdminNotification.objects.filter(parent=parent).select_related('student__admin').order_by('-created_at')

    session = Session.objects.filter(is_active=True).first()

    context = {
        'user': request.user,
        'parent': parent,
        'page_title': 'Parent Dashboard',
        'students': students,
        'total_students': students.count() if hasattr(students, 'count') else len(students),
        'notifications': notifications,
        'total_notifications': notifications.count() if hasattr(notifications, 'count') else len(notifications),
        'session': session,
    }

    return render(request, 'Parent_template/parent_home.html', context)

def parent_student_detail(request, student_id):
    """
    Display detailed information about a student for the parent.
    """
    if request.user.user_type != '6':
        return redirect('login_page')
    
    # Get the parent object for the logged-in user
    parent = Parent.objects.filter(admin=request.user).first()
    # Get the student and verify they belong to this parent
    student = get_object_or_404(Student, id=student_id)

    # Verify the student belongs to this parent
    is_linked = (parent and student.parents == parent) or (parent and ParentAdminNotification.objects.filter(student=student, parent=parent).exists())
    if is_linked:
        # Get results organized by exam_type (TP1, TP2, PT1, etc.)
        from collections import defaultdict
        results_by_exam = defaultdict(list)
        
        results = StudentResult.objects.filter(student=student).order_by('exam_type__exam_date', 'created_at')
        
        for result in results:
            exam_name = result.exam_type.exam_name if result.exam_type else "Unknown"
            results_by_exam[exam_name].append(result)
        
        # Convert to ordered list
        results_data = [{'exam_name': exam_name, 'results': res} 
                       for exam_name, res in results_by_exam.items()]
        
        # Get attendance data by subject
        attendance_by_subject = defaultdict(lambda: {'total': 0, 'present': 0})
        
        attendance_records = Attendance.objects.filter(
            subject__course=student.course
        ).select_related('subject__subject')
        
        for attendance in attendance_records:
            subject_name = attendance.subject.subject.name if attendance.subject and attendance.subject.subject else "Unknown"
            attendance_by_subject[subject_name]['total'] += 1
        
        attendance_data = [{'subject': subject, 'data': stats} 
                          for subject, stats in attendance_by_subject.items()]
        
        context = {
            'student': student,
            'parent': parent,
            'page_title': f'{student.admin.first_name} {student.admin.last_name} - Details',
            'results_data': results_data,
            'attendance_data': attendance_data
        }
        return render(request, 'Parent_template/parent_student_detail.html', context)
    else:
        # Student does not belong to this parent
        messages.error(request, 'Student data is not available.')
        return redirect('parent_home')

# def submit_student_notification(request):
#     """
#     Handle parent submission of student details to create a notification.
#     """
#     if request.method == 'POST' and request.user.user_type == '6':
#         try:
#             student_name = request.POST.get('student_name', '').strip()
#             admission_number = request.POST.get('admission_number', '').strip()
            
#             if not student_name or not admission_number:
#                 messages.error(request, 'Please provide both student name and admission number.')
#                 return redirect('parent_home')
            
#             # Get the parent object
#             parent = Parent.objects.get(admin=request.user)
            
#             # Create the message with student name and admission number
#             notification_message = f'Student Name: {student_name}, Admission Number: {admission_number}'
            
#             # Save to ParentAdminNotification table
#             ParentAdminNotification.objects.create(
#                 parent=parent,
#                 message=notification_message
#             )
            
#             messages.success(request, 'Your student details have been submitted successfully.')
#             return redirect('parent_home')
        
#         except Parent.DoesNotExist:
#             messages.error(request, 'Parent record not found.')
#             return redirect('parent_home')
#         except Exception as e:
#             messages.error(request, f'An error occurred: {str(e)}')
#             return redirect('parent_home')
#     else:
#         return redirect('parent_home')
def submit_student_notification(request):

    if request.method == 'POST' and request.user.user_type == '6':
        try:
            student_name = request.POST.get('student_name', '').strip()
            print('student_name',student_name)
            # Split by space or dot (one or more)
            parts = re.split(r'[.\s]+', student_name)

            first_name = parts[0] if len(parts) > 0 else ''
            last_name  = parts[-1] if len(parts) > 1 else ''
            admission_number = request.POST.get('admission_number', '').strip()
           
            if not student_name or not admission_number:
                messages.error(request, 'Please provide both student name and admission number.')
                return redirect('parent_home')

            # ✅ Get Parent
            parent = Parent.objects.get(admin=request.user)

            # ✅ Step 1: Check student exists in CustomUser

            # student_user = CustomUser.objects.filter(
            #     first_name__iexact=first_name,
            #     last_name__iexact=last_name,
            #     user_type='3'   # 3 = student
            # ).first()
            # print('student_user',student_user)
            student_user = CustomUser.objects.filter(
             Q(first_name__iexact=student_name) | Q(last_name__iexact=student_name),
              user_type='3'
             ).first()
           
            if not student_user:
                messages.error(request, 'Student not found in user records.')
                return redirect('parent_home')

            # ✅ Step 2: Get student from Student table using admin_id
            student = Student.objects.filter(admin=student_user).first()

            if not student:
                messages.error(request, 'Student record not found.')
                return redirect('parent_home')

            # ✅ Step 3: Verify admission number
            if student.admission_number.strip().lower() != admission_number.strip().lower():
                messages.error(request, 'Admission number does not match.')
                return redirect('parent_home')

            # ✅ Step 4: Save notification
            ParentAdminNotification.objects.create(
                parent=parent,
                student=student,
                message="Student verification request submitted.",
                status="Pending"
            )

            messages.success(request, 'Student verification request submitted successfully.')
            return redirect('parent_home')

        except Parent.DoesNotExist:
            messages.error(request, 'Parent record not found.')
            return redirect('parent_home')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('parent_home')

    return redirect('parent_home')

def student_search(request):
    if request.user.user_type != '6':
        return redirect('login_page')
    parent = Parent.objects.filter(admin=request.user).first()
    students = Student.objects.filter(parents=parent).select_related('admin', 'course', 'session') if parent else []
    notifications = ParentAdminNotification.objects.filter(parent=parent).select_related('student__admin').order_by('-created_at') if parent else []
    context = {
        'page_title': 'Search & Link Ward',
        'students': students,
        'parent': parent,
        'notifications': notifications,
    }
    return render(request, 'Parent_template/student_search.html', context)