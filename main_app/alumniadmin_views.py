import json
import os
import smtplib
import random
from email.mime.text import MIMEText
from django.conf import settings
from django.db import IntegrityError
from main_app.models import Subject, Course, Subjectmaster,School
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from openpyxl.utils import get_column_letter
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
import requests
from django.templatetags.static import static
from django.views.generic import UpdateView
from openpyxl import load_workbook
from .models import Student
from .forms import AccAdminForm
from .forms import AlumniAdminForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from .models import CustomUser
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
import openpyxl
import pandas as pd
from .forms import ExcelUploadForm
from django.shortcuts import render
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from io import BytesIO
from .models import Student
from openpyxl.utils.dataframe import dataframe_to_rows  # Correct import
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import smtplib
from email.mime.text import MIMEText
import traceback
from datetime import datetime


# Helper function for authentication checks
def is_admin(user):
    return user.is_authenticated and user.user_type == '7'


@login_required
def alumniadmin_home(request):
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    # subjects = Subjectmaster.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        # subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
        
    # Alumni Module Statistics & Recent Data
    total_alumni = Alumnimembers.objects.count()
    pending_alumni = Alumnimembers.objects.filter(is_active=False).count()
    active_alumni = Alumnimembers.objects.filter(is_active=True).count()
    total_events = AlumniEventsInfo.objects.count()
    total_jobpostings = CareerInfo.objects.count()
    total_companies = AssociatedCompanies.objects.count()
    total_guidance = CareerGuidance.objects.count()
    total_feedback = AlumniFeedback.objects.count()

    recent_alumni = Alumnimembers.objects.select_related('admin', 'course').order_by('-id')[:6]
    recent_events = AlumniEventsInfo.objects.all().order_by('-id')[:4]
    recent_jobs = CareerInfo.objects.all().order_by('-id')[:4]
       
    context = {
        'page_title': "Alumni Admin Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'subjects': subjects,
        'courses': courses,
        # Alumni metrics
        'total_alumni': total_alumni,
        'pending_alumni': pending_alumni,
        'active_alumni': active_alumni,
        'total_events': total_events,
        'total_jobpostings': total_jobpostings,
        'total_companies': total_companies,
        'total_guidance': total_guidance,
        'total_feedback': total_feedback,
        'recent_alumni': recent_alumni,
        'recent_events': recent_events,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'alumniadmin_template/home_content.html', context)
def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Teacher'}
    if request.method == 'POST':

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            city = form.cleaned_data.get('city')
            district_name =form.cleaned_data.get('district_name')
            street_address = form.cleaned_data.get('street_address')
            state =form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            gender = form.cleaned_data.get('gender')
            department = form.cleaned_data.get('department')
            course = form.cleaned_data.get('course')
            date_of_birth=form.cleaned_data['date_of_birth']
            contact_number = form.cleaned_data['contact_number']
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url, date_of_birth=date_of_birth)
                user.gender = gender
                user.street_add = street_address
                user.city = city
                user.state = state
                user.district_name = district_name
                user.country = country
                user.staff.course = course
                user.staff.department = department
                user.date_of_birth= date_of_birth
                user.contact_number = contact_number
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")

    return render(request, 'alumniadmin_template/add_staff_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student Profile'}
    if request.method == 'POST':
       if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            admission_number = student_form.cleaned_data.get('admission_number')
            email = student_form.cleaned_data.get('email')
            password = student_form.cleaned_data.get('password')
            gender = student_form.cleaned_data.get('gender')
            course = student_form.cleaned_data.get('course')
            session = student_form.cleaned_data.get('session')
            city = student_form.cleaned_data.get('city')
            district_name =student_form.cleaned_data.get('district_name')
            street_address = student_form.cleaned_data.get('street_address')
            state =student_form.cleaned_data.get('state') 
            country = student_form.cleaned_data.get('country')
            #religion=StudentForm.cleaned_data.get('religion')
            parent_name = student_form.cleaned_data.get('parent_name')
            guardian_contact_number = student_form.cleaned_data.get('guardian_contact_number')
            mother_name = student_form.cleaned_data.get('mother_name')
            blood_group = student_form.cleaned_data.get('blood_group')
            mother_tongue = student_form.cleaned_data.get('mother_tongue')
            passport = request.FILES['profile_pic']
            date_of_birth=student_form.cleaned_data['date_of_birth']
             # Check if admission number already exists
            if CustomUser.objects.filter(student__admission_number=admission_number).exists():
                messages.error(request, "Admission number already exists.")
                return render(request, 'hod_template/add_student_template.html', context)

            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url, date_of_birth=date_of_birth )
                user.gender = gender
                user.street_address = street_address
                user.city = city
                user.state=state
                user.district_name = district_name
                user.country = country
                user.student.session = session
                user.student.course = course
                user.student.admission_number = admission_number
                user.student.parent_name = parent_name
                user.student.guardian_contact_number = guardian_contact_number
                user.student.mother_name = mother_name
                user.student.blood_group = blood_group
                user.student.mother_tongue = mother_tongue
                user.student.date_of_birth= date_of_birth
                #user.student.religion= religion

                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        #else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_student_template.html', context)

def add_acc_admin(request):
    accadmin_form = AccAdminForm(request.POST or None, request.FILES or None)
    context = {'form': accadmin_form, 'page_title': 'Add Academic Admin'}
    if request.method == 'POST':

        if accadmin_form.is_valid():
            first_name = accadmin_form.cleaned_data.get('first_name')
            last_name = accadmin_form.cleaned_data.get('last_name')
            city = accadmin_form.cleaned_data.get('city')
            district_name =accadmin_form.cleaned_data.get('district_name')
            street_address = accadmin_form.cleaned_data.get('street_address')
            state =accadmin_form.cleaned_data.get('state')
            country = accadmin_form.cleaned_data.get('country')
            email = accadmin_form.cleaned_data.get('email')
            password = accadmin_form.cleaned_data.get('password')
            gender = accadmin_form.cleaned_data.get('gender')
            date_of_birth=accadmin_form.cleaned_data['date_of_birth']
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=4, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_acc_admin'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")

    return render(request, 'alumniadmin_template/add_acc_admin_template.html', context)



def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course & Batch'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            batch = form.cleaned_data.get('batch')
            try:
                # Check for duplicates

                if Course.objects.filter(name=name, batch=batch).exists():



                    messages.error(request, "Course with the same name and batch already exists.")
                else:
                    # Create and save the new course
                    course = Course()
                    course.name = name
                    course.batch = batch
                    course.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add_course'))
            except Exception as e:
                messages.error(request, f"Could Not Add: {str(e)}")
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'alumniadmin_template/add_course_template.html', context)

def add_department(request):
 form = DepartmentForm(request.POST or None)
 context = {
        'form': form,
        'page_title': 'Add Department'
    }
 if request.method == 'POST':
        if form.is_valid():
            course = form.cleaned_data.get('course')
            name = form.cleaned_data.get('department')
            # print(course,department)
            try:
                # Check for duplicates
                if Department.objects.filter(course=course, department=name).exists():
                    messages.error(request, "Deparment with the same course and department already exists.")
                else:
                    # Create and save the new department
                    department = Department()
                    department.course = course
                    department.department = name
                    department.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add_department'))
            except Exception as e:
                messages.error(request, f"Could Not Add: {str(e)}")
        else:
            messages.error(request, "Fill Form Properly")
 return render(request, 'alumniadmin_template/add_department_template.html',context)





def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Subject Assign'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('subject')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                # Check for duplicates
                if Subject.objects.filter(subject=name, course=course, staff=staff).exists():
                    messages.error(request, "Subject with the same name, course, and staff already exists.")
                else:
                    # Create and save a new subject
                    subject = Subject()
                    subject.subject = name
                    subject.staff = staff
                    subject.course = course
                    subject.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add_subject'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'alumniadmin_template/add_subject_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Teacher'
    }
    return render(request, "alumniadmin_template/manage_staff.html", context)

def manage_acc_admin(request):
    allacademicAdmin = CustomUser.objects.filter(user_type=4)
   
    context = {
        'allacademicAdmin': allacademicAdmin,
        'page_title': 'Manage Academic Admin'
    }
    return render(request, "hod_alumniadmin_templatetemplate/manage_acc_admin.html", context)


def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    return render(request, "alumniadmin_template/manage_student.html", context)


def manage_course(request):
    courses = Course.objects.all()
    message = request.GET.get('message', '')
    message_type = request.GET.get('message_type', '')
    context = {
        'courses': courses,
        'page_title': 'Manage Course & Batch',
        'message': message,
        'message_type': message_type
    }
    return render(request, "alumniadmin_template/manage_course.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subject Assign'
    }
    return render(request, "alumniadmin_template/manage_subject.html", context)


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Teacher'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            city = form.cleaned_data.get('city')
            district_name =form.cleaned_data.get('district_name')
            street_address = form.cleaned_data.get('street_address')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            contact_number = form.cleaned_data.get('contact_number')
            department = form.cleaned_data.get('department')
            passport = request.FILES.get('profile_pic') #or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.street_address = street_address
                user.city = city
                user.state = state
                user.district_name = district_name
                user.country = country
                staff.course = course
                staff.contact_number = contact_number
                staff.department = department

                user.save()
                staff.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "alumniadmin_template/edit_staff_template.html", context)    

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None,  instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':

        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            city = form.cleaned_data.get('city')
            district_name =form.cleaned_data.get('district_name')
            state = form.cleaned_data.get('state')
            street_address = form.cleaned_data.get('street_address')
            country = form.cleaned_data.get('country')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            admission_number = form.cleaned_data.get('admission_number')
            parent_name = form.cleaned_data.get('parent_name')
            mother_tongue =form.cleaned_data.get('mother_tongue')
            date_of_birth=form.cleaned_data['date_of_birth']
            passport = request.FILES.get('profile_pic')
            try:

                user = CustomUser.objects.get(id=student.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.session = session
                user.gender = gender
                user.city = city
                user.state = state
                user.district_name = district_name
                user.country = country
                user.street_address = street_address
                student.course = course
                student.admission_number = admission_number
                student.parent_name = parent_name
                student.mother_tongue = mother_tongue
                student.date_of_birth= date_of_birth
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fill out the form properly!")
            return render(request, "alumniadmin_template/edit_student_template.html", context)
            # messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "alumniadmin_template/edit_student_template.html", context)

def students_list(request):
    query = request.GET.get('q', '').strip()
    students = CustomUser.objects.filter(user_type="3")
    if query:
        gender_query = query.upper() if query.upper() in ["M", "F", "O"] else None
        filters = (
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(city__icontains=query) |
            Q(district_name__icontains=query) |
            Q(student__course__name__icontains=query) |
            Q(student__course__division__icontains=query)
        )
        if gender_query:
            filters |= Q(gender__iexact=gender_query)
        students = students.filter(filters).distinct()
    context = {
        'page_title': 'Students List',
        'students': students
    }
    return render(request, "alumniadmin_template/students_list_template.html", context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': course_id,
        'page_title': 'Edit Course & Batch'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            batch = form.cleaned_data.get('batch')
            try:
                if  Course.objects.filter(name=name, batch=batch).exists():
                    messages.error(request, "Course with the same name and batch already exists.")
                else:
                    course = Course.objects.get(id=course_id)
                    course.name = name
                    course.batch = batch
                    course.save()
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_course_template.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('subject')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.subject = name
                subject.staff = staff
                subject.course = course
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'alumniadmin_template/edit_subject_template.html', context)


def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Academmic Year'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "alumniadmin_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Academic Year'}
    return render(request, "alumniadmin_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Academic Year'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Academmic  Year Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "alumniadmin_template/edit_session_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def student_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'hod_template/student_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'alumniadmin_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Staff'
        }
        return render(request, "alumniadmin_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_student_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Students'
        }
        return render(request, "alumniadmin_template/student_leave_view.html", context)
        return render(request, "/student_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "alumniadmin_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.student)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


@login_required
def alumniadminviewprofile(request):
    try:
        alumni_admin_obj = get_object_or_404(AlumniAdmin, alumniadmin=request.user)
        import logging
        logger = logging.getLogger(__name__)
        logger.debug('alumni_admin_obj: %s', alumni_admin_obj)
        custom_user = alumni_admin_obj.alumniadmin
        logger.debug('custom_user: %s', custom_user)  # CustomUser instance
    except Exception as e:
        messages.error(request, f"AlumniAdmin Profile Not Found: {e}")
        return redirect('alumniadminviewprofile')  # Or fallback

    form = AlumniAdminForm(request.POST or None, request.FILES or None, instance=alumni_admin_obj)
    logger.debug('form sdfs: %s', form)
    if request.method == 'POST':
        if form.is_valid():
            user = alumni_admin_obj.alumniadmin

            for field in ('first_name', 'last_name', 'email', 'gender', 'street_address',
                          'city', 'district_name', 'state', 'country', 'date_of_birth'):
                setattr(user, field, form.cleaned_data.get(field))

            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            passport = request.FILES.get('profile_pic')
            user.save()
            if passport:
                save_user_profile_pic(passport, user)
            if password:
                update_session_auth_hash(request, user)
            alumni_admin_obj.year_of_passing = form.cleaned_data.get('year_of_passing')
            alumni_admin_obj.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect(reverse('alumniadminviewprofile'))
        else:
            messages.error(request, "Invalid Data Provided")

    context = {
        'form': form,
        'page_title': 'View/Edit Profile'
    }

    return render(request, "alumniadmin_template/admin_view_profile.html", context)

def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "alumniadmin_template/staff_notification.html", context)


def admin_notify_student(request):
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, "hod_template/student_notification.html", context)


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Alumni Management System",
                'body': message,
                'click_action': reverse('student_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, "Teacher deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    has_department = Department.objects.filter(course=course).exists()
    has_alumni = Alumnimembers.objects.filter(course=course).exists()

    if has_department or has_alumni:
        if has_department and not has_alumni:
            messages.error(request, "This course cannot be deleted because it has associated departments.")
            return redirect(reverse('manage_course'))
        if has_department and has_alumni:
            messages.error(request, "This course cannot be deleted because it has associated departments and alumni members.")
            return redirect(reverse('manage_course'))

    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect(reverse('manage_course'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Academmic  Year deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))

def delete_allAdmin(request,allAdmin_id):
     academic_delete = CustomUser.objects.get(id=allAdmin_id)
     academic_delete.delete()
     messages.success(request, "Successfully Deleted")
     return redirect(reverse('manage_alumni_admin'))

def import_from_excel(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':#and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']


# ... rest of the code ...

def import_from_excel(request):
    if request.method == "POST":
         student_form = StudentForm(request.POST, request.FILES )
         context = {'form': student_form, 'page_title': 'Add Student'}
         if student_form.is_valid():
              excel_file = student_form.cleaned_data['excel_file']
              workbook = openpyxl.load_workbook(excel_file)
              worksheet = workbook.active
         for row in worksheet.iter_rows(min_row=2, values_only=True):
              first_name,last_name,email,gender,password,course,session,admission_number,parent_name,mother_tongue,passport=row
              excel_file = request.FILES['excel_file']

         first_name = row['first_name']
         last_name = row['last_name']
         #address = row['address']
         email = row['email']
         gender = row['gender']
         password = row['password']
         course = row['course']
         session = row['session']
         admission_number = row['admission_number']
         parent_name = row['parent_name']
         mother_tongue = row['mother_tongue']
         passport = request.FILES['profile_pic']
         fs = FileSystemStorage()
         filename = fs.save(passport.name, passport)
         passport_url = fs.url(filename)
            # Create a new student object and save it to the database
         student = Student(
                first_name=first_name,
                last_name=last_name,
                #address=address,
                email=email,
                gender=gender,
                password=password,
                course=course,
                session=session,
                admission_number=admission_number,
                parent_name=parent_name,
                mother_tongue=mother_tongue,
                profile_pic=passport_url
            )
         student.save()
         messages.success(request, 'Student added successfully!')
         return redirect(reverse('manage_student'))
    return render(request, 'alumniadmin_template/add_student_template.html', context)
def add_college(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address=form.cleaned_data.get('address')
            city=form.cleaned_data.get('city')
            state=form.cleaned_data.get('state')
            country=form.cleaned_data.get('country')
            phone=form.cleaned_data.get('phone')
            email=form.cleaned_data.get('email')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image = fs.url(filename)
            if School.objects.filter(name=name).exists():
                messages.error(request, "College already exists.")
            else:
                school = School()
                school.name = name
                school.address = address
                school.city = city
                school.state = state
                school.country = country
                school.phone = phone
                school.email = email
                image = request.FILES.get('image')
                
                school.image = image
                school.save()
                messages.success(request, "College successfully added.")
                return redirect(reverse('add_college'))
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = SchoolForm()

    context = {
        'form': form,
        'page_title': 'Add College Profile'
    }
    return render(request, 'alumniadmin_template/add_school_template.html', context)

def  manage_college(request):
 school = School.objects.all()
 context = {
        'school': school,
        'page_title': 'Manage  College Profile'
    }
 return render(request, 'alumniadmin_template/manage_school_template.html',context )   

def edit_college(request,school_id):
    instance = get_object_or_404(School, id=school_id)
    form = SchoolForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'school_id': school_id,
        'page_title': 'Edit College Profile'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address=form.cleaned_data.get('address')
            city=form.cleaned_data.get('city')
            state=form.cleaned_data.get('state')
            country=form.cleaned_data.get('country')
            phone=form.cleaned_data.get('phone')
            email=form.cleaned_data.get('email')
            image=form.cleaned_data.get('image')
            try:
                    school = School.objects.get(id=school_id)
                    school.name = name
                    school.address = address
                    school.city = city
                    school.state = state
                    school.country = country
                    school.phone = phone
                    school.email = email
                    image = request.FILES.get('image')
                    if image:
                        # Save the new image
                        fs = FileSystemStorage()
                        filename = fs.save(image.name, image)
                        school.image = image  # Assign the new image
                    else:
                        # Keep the existing image (do nothing)
                        messages.info(request, "No new image selected. Retaining the existing image.")

                        # Save the updated school object
                    school.save()
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_school_template.html',context ) 
def delete_college(request, school_id):
    school = get_object_or_404(School, id=school_id)
    school.delete()
    messages.success(request, "College Profile deleted successfully!")
    return redirect(reverse('manage_college'))



def add_alumniadmin(request):
    if request.method == 'POST':
        form = AlumnimembersForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data

                # profile picture
                passport_url = None
                if 'profile_pic' in request.FILES:
                    passport = request.FILES['profile_pic']
                    profile_storage = FileSystemStorage(
                        location=os.path.join(settings.MEDIA_ROOT, 'profiles')
                    )
                    filename = profile_storage.save(passport.name, passport)
                    passport_url = os.path.join('profiles', filename)

                otp_password = str(random.randint(100000, 999999))

                # Check if email already exists
                if CustomUser.objects.filter(email=data['email']).exists():
                    messages.error(request, "User with this email already exists.")
                    return redirect(reverse('add_alumni'))

                # Create user
                user = CustomUser.objects.create_user(
                    email=data['email'],
                    password=otp_password,
                    user_type='5',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    profile_pic=passport_url,
                    date_of_birth=data['date_of_birth'],
                    gender=data['gender'],
                    city=data['city'],
                    state=data['state'],
                    district_name=data['district_name'],
                    country=data['country'],
                    street_address=data['street_address'],
                )
                user.otp = otp_password
                user.save()

                # Prevent duplicate alumni
                # if Alumnimembers.objects.filter(admin=user).exists():
                #     messages.error(request, "This alumni record already exists.")
                #     return redirect(reverse('add_alumni'))

                # Create alumni
                alumni = Alumnimembers.objects.create(
                    admin=user,
                    mobile=data['mobile'],
                    period_of_study=data['period_of_study'],
                    employment_status=data['employment_status'],
                    employment_remarks=data['employment_remarks'],
                    employment_sectors=data['employment_sectors'],
                    current_street_address=data['current_street_address'],
                    current_district_name=data['current_district_name'],
                    current_state=data['current_state'],
                    current_city=data['current_city'],
                    course_studied=data['course_studied'],
                    on_campus_achievements=data['on_campus_achievements'],
                    beyond_college_achievements=data['beyond_college_achievements'],
                    outside_institution_course=data['outside_institution_course'],
                    contribution=data['contribution'],
                    mode_of_payment=data['mode_of_payment'],
                    membershipfees=data['membershipfees'],
                    willingness=data['willingness'],
                    is_active=data['is_active'],
                    course=data['course'],
                    department=data['department']
                )
                alumni.save()
                # Send email
                subject = "Your Alumni Login Details"
                message = f"""
Dear {user.first_name} {user.last_name},

Your alumni account has been successfully created.

Here are your login credentials:

Email: {user.email}
Password: {otp_password}

Please log in at the portal and change your password for better security.

Thank you,
College Admin
"""
                try:
                    msg = MIMEText(message)
                    msg['Subject'] = subject
                    msg['From'] = 'alumniimentor@gmail.com'
                    msg['To'] = user.email

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('alumniimentor@gmail.com', 'lznjeuvbdpsozqim')
                    server.send_message(msg)
                    server.quit()
                except Exception as mail_error:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.exception('Error sending email while notifying alumniadmin creation')
                    messages.warning(request, "Alumni added but email failed to send.")

                messages.success(request, "Alumni added and login credentials sent via email.")
                return redirect(reverse('add_alumniadmin'))

            except Exception as e:
                traceback.print_exc()
                messages.error(request, f"Could not add alumni: {str(e)}")
        else:
            messages.error(request, "Form contains errors. Please correct them.")
    else:
        form = AlumnimembersForm()

    return render(request, 'alumniadmin_template/alumini_template.html', {
        'form': form,
        'page_title': 'Add Alumni'
    })

@csrf_exempt
def get_alumini_course(request):
    course = request.POST.get('course')
    alumini_department = Department.objects.filter(course=course)
    subject_data = []
    for department in alumini_department:
        data = {
                 "id": department.id,
                 "department": department.department 
                }
        subject_data.append(data) 
    return JsonResponse(json.dumps(subject_data), content_type='application/json', safe=False)
def manage_alumniadmin(request):
    alumini = CustomUser.objects.filter(
    user_type=5
)  
    # print(alumini)
    form = AlumnimembersForm(request.POST or None,request.FILES or None)
    context = {
        'form' : form,
        'alumini': alumini,
        'page_title': 'Manage Alumni'
    }
    return render(request,'alumniadmin_template/manage_alumini_template.html',context)

def manage_department(request):
    department = Department.objects.all()
    form = DepartmentForm(request.POST or None,request.FILES or None)
    context = {
        'form' : form,
        'department': department,
        'page_title': 'Manage Department'
        }
    return render(request,'alumniadmin_template/manage_department_template.html',context)
def edit_department(request,id):
    # id = request.GET.get('id')
   
    department = Department.objects.get(id=id)
    form = DepartmentForm(request.POST or None,instance=department)
    if form.is_valid():
        form.save()
        return redirect('manage_department')
    context = {
        'form' : form,
        'department': department,
        'page_title': 'Edit Department'
        }
    return render(request,'alumniadmin_template/edit_department_template.html',context)

def delete_department(request,dept_id):
    department = get_object_or_404(Department, id=dept_id)
    course = department.course  # Get associated course

    has_course = Course.objects.filter(name=course).exists()
    has_alumni = Alumnimembers.objects.filter(department=department).exists()

    if has_course or has_alumni:
        if has_course and has_alumni:
            messages.error(request, "This department cannot be deleted because it has associated courses and alumni members.")
            return redirect(reverse('manage_department'))
        
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect(reverse('manage_department'))

    
@csrf_exempt
def approve_alumini(request):
    if request.method == "POST":
        alumni_id = request.POST.get("id")
        try:
            alumni = Alumnimembers.objects.get(id=alumni_id)
            alumni.is_active = True
            alumni.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Alumni not found"}, status=400)
    return redirect(reverse("manage_alumni1"))

# def editalumini(request, alumini_id):
#     # Fetch the alumni settings object using admin__id
#     alumni = get_object_or_404(Alumnimembers, admin__id=alumini_id)
#     user = alumni.admin  # Get the linked CustomUser object

#     form = AlumnimembersForm(request.POST or None, request.FILES or None, instance=alumni)

#     context = {
#         'form': form,
#         'alumini_id': alumini_id,
#         'page_title': 'Edit Alumni'
#     }

#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 # Extract user details from the form
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 email = form.cleaned_data.get('email')
#                 password = form.cleaned_data.get('password') or None
#                 gender = form.cleaned_data.get('gender')
#                 city = form.cleaned_data.get('city')
#                 state = form.cleaned_data.get('state')
#                 district_name = form.cleaned_data.get('district_name')
#                 country = form.cleaned_data.get('country')
#                 street_address = form.cleaned_data.get('street_address')
#                 course = form.cleaned_data.get('course')
#                 mobile = form.cleaned_data.get('mobile')
#                 current_street_address = form.cleaned_data.get('current_street_address')
#                 current_city = form.cleaned_data.get('current_city')
#                 current_district_name = form.cleaned_data.get('current_district_name')
#                 current_state = form.cleaned_data.get('current_state')
#                 current_course = form.cleaned_data.get('current_course')
#                 current_department = form.cleaned_data.get('current_department')
#                 current_period_of_study = form.cleaned_data.get('current_period_of_study')
#                 employment_status = form.cleaned_data.get('employment_status')
#                 employment_remarks = form.cleaned_data.get('employment_remarks')
#                 employment_sectors = form.cleaned_data.get('employment_sectors')
#                 course_studied = form.cleaned_data.get('course_studied')
#                 on_campus_achievements = form.cleaned_data.get('on_campus_achievements')
#                 beyond_college_achievements = form.cleaned_data.get('beyond_college_achievements')
#                 outside_institution_course = form.cleaned_data.get('outside_institution_course')
#                 contribution = form.cleaned_data.get('contribution')
#                 mode_of_payment = form.cleaned_data.get('mode_of_payment')
#                 membershipfees = form.cleaned_data.get('membershipfees')
#                 willingness = form.cleaned_data.get('willingness')
#                 is_active = form.cleaned_data.get('is_active')

#                 # Handle profile picture update
#                 passport = request.FILES.get('profile_pic')
#                 if passport:
#                     fs = FileSystemStorage()
#                     filename = fs.save(passport.name, passport)
#                     passport_url = fs.url(filename)
#                     user.profile_pic = passport_url

#                 # Update CustomUser fields
#                 user.first_name = first_name
#                 user.last_name = last_name
#                 user.email = email
#                 user.gender = gender
#                 user.city = city
#                 user.state = state
#                 user.district_name = district_name
#                 user.country = country
#                 user.street_address = street_address
#                 user.course = course

                

#                 if password:
#                     user.set_password(password)  # Hash password

#                 user.save()  # Save changes to CustomUser

#                 # Update alumnimembers fields
#                 alumni.mobile = form.cleaned_data.get('mobile')
#                 alumni.current_street_address = form.cleaned_data.get('current_street_address')
#                 alumni.current_city = form.cleaned_data.get('current_city')
#                 alumni.current_district_name = form.cleaned_data.get('current_district_name')
#                 alumni.current_state = form.cleaned_data.get('current_state')
#                 alumni.course = form.cleaned_data.get('course')
#                 alumni.department = form.cleaned_data.get('department')
#                 alumni.period_of_study = form.cleaned_data.get('period_of_study')
#                 alumni.employment_status = form.cleaned_data.get('employment_status')
#                 alumni.employment_remarks = form.cleaned_data.get('employment_remarks')
#                 alumni.employment_sectors = form.cleaned_data.get('employment_sectors')
#                 alumni.course_studied = form.cleaned_data.get('course_studied')
#                 alumni.on_campus_achievements = form.cleaned_data.get('on_campus_achievements')
#                 alumni.beyond_college_achievements = form.cleaned_data.get('beyond_college_achievements')
#                 alumni.outside_institution_course = form.cleaned_data.get('outside_institution_course')
#                 alumni.contribution = form.cleaned_data.get('contribution')
#                 alumni.mode_of_payment = form.cleaned_data.get('mode_of_payment')
#                 alumni.membershipfees = form.cleaned_data.get('membershipfees')
#                 alumni.willingness = form.cleaned_data.get('willingness')
#                 alumni.is_active = form.cleaned_data.get('is_active')

#                 alumni.save()  # Save changes to alumnimembers

#                 messages.success(request, "Successfully Updated Alumni")
#                 return redirect(reverse('editalumini', args=[alumini_id]))

#             except Exception as e:
#                 messages.error(request, "Could Not Update: " + str(e))
#         else:
#             messages.error(request, "Form contains errors, please check your inputs.")

#     return render(request, 'alumniadmin_template/edit_alumini_template.html', context)


def manage_alumni_admin(request):
    alumni_Admin = CustomUser.objects.filter(user_type=6)
   
    context = {
        'alumni_Admin': alumni_Admin,
        'page_title': 'Manage Alumni Admin'
    }
    return render(request, "alumniadmin_template/manage_alumni_admin.html", context)

# def add_alumni1(request):
#     form = AlumniMembersForm(request.POST or None,request.FILES or None)
#     context = {
#         'form': form,
#         'page_title': 'Add Alumini'
#     }
#     if request.method == 'POST':
#         if form.is_valid():
#             studentname = form.cleaned_data.get('studentname')
#             gender = form.cleaned_data.get('gender')
#             email = form.cleaned_data.get('email')
#             mobile = form.cleaned_data.get('mobile')
#             if not mobile.isdigit() or len(mobile) != 10:
#                 messages.error(request, "Mobile number must be exactly 10 digits.")
#             else:
            
#              permanent_locality = form.cleaned_data.get('permanent_locality')
#             permanent_district = form.cleaned_data.get('permanent_district')
#             permanent_state = form.cleaned_data.get('permanent_state')
#             same_as_permanent = form.cleaned_data.get('same_as_permanent')
#             current_locality = form.cleaned_data.get('current_locality')
#             current_district = form.cleaned_data.get('current_district')
#             current_state = form.cleaned_data.get('current_state')
#             course_studied = form.cleaned_data.get('course_studied')
#             period_of_study = form.cleaned_data.get('period_of_study')
#             current_status = form.cleaned_data.get('current_status')
#             is_active = form.cleaned_data.get('is_active')
#             passport = request.FILES.get('image')
#             fs = FileSystemStorage()
#             filename = fs.save(passport.name, passport)
#             passport_url = fs.url(filename)
           
#             try:
#                 # Check for duplicates
#                 if Alumnimembers.objects.filter(email=email).exists():
#                     messages.error(request, "Student with the same email already exists.")
#                 else:
#                     # Create and save the new course
#                      alumini = Alumnimembers()
#                      alumini.studentname = studentname
#                      alumini.gender = gender
#                      alumini.email = email
#                      alumini.mobile = mobile
#                      alumini.permanent_locality = permanent_locality
#                      alumini.permanent_district = permanent_district
#                      alumini.permanent_state = permanent_state
#                      alumini.current_locality = current_locality
#                      alumini.current_district = current_district
#                      alumini.current_state = current_state
#                      alumini.course_studied = course_studied
#                      alumini.period_of_study = period_of_study
#                      alumini.current_status = current_status
#                      alumini.image = passport_url
#                      alumini.is_active = is_active
#                      alumini.save()
#                      messages.success(request, "Successfully Added")
#                      return redirect(reverse('add_alumni1'))
#             except Exception as e:
#                  messages.error(request, f"Could Not Add: {str(e)}")
#         else:
#             messages.error(request, "Please correct the following errors!")
#     return render(request,'alumniadmin_template/alumini_template.html',context)
def add_alumni1(request):
    try:
        passing_year = request.user.alumniadmin.year_of_passing
    except AlumniAdmin.DoesNotExist:
        passing_year = None

    if request.method == 'POST':
        form = AlumniMembersForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data

                # profile picture
                passport_url = None
                passport = request.FILES.get('profile_pic')

                otp_password = str(random.randint(100000, 999999))

                # Check if email already exists
                if CustomUser.objects.filter(email=data['email']).exists():
                    messages.error(request, "User with this email already exists.")
                    return redirect(reverse('aadd_alumni1'))

                # Create user
                user = CustomUser.objects.create_user(
                    email=data['email'],
                    password=otp_password,
                    user_type='8',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    profile_pic=None,
                    date_of_birth=data['date_of_birth'],
                    gender=data['gender'],
                    city=data['city'],
                    state=data['state'],
                    district_name=data['district_name'],
                    country=data['country'],
                    street_address=data['street_address'],
                )
                user.otp = otp_password
                user.save()
                if passport:
                    save_user_profile_pic(passport, user)

                # Create or update the alumni profile for this user
                alumni, _ = Alumnimembers.objects.get_or_create(admin=user)
                alumni.mobile = data['mobile']
                alumni.period_of_study = data['period_of_study']
                alumni.employment_status = data['employment_status']
                alumni.employment_remarks = data['employment_remarks']
                alumni.employment_sectors = data['employment_sectors']
                alumni.current_street_address = data['current_street_address']
                alumni.current_district_name = data['current_district_name']
                alumni.current_state = data['current_state']
                alumni.current_city = data['current_city']
                alumni.course_studied = data['course_studied']
                alumni.on_campus_achievements = data['on_campus_achievements']
                alumni.beyond_college_achievements = data['beyond_college_achievements']
                alumni.outside_institution_course = data['outside_institution_course']
                alumni.contribution = data['contribution']
                alumni.mode_of_payment = data['mode_of_payment']
                alumni.membershipfees = data['membershipfees']
                alumni.willingness = data['willingness']
                alumni.is_active = data['is_active']
                alumni.course = data['course']
                alumni.department = data['department']
                alumni.save()
                # Send email
                subject = "Your Alumni Login Details"
                message = f"""
Dear {user.first_name} {user.last_name},

Your alumni account has been successfully created.

Here are your login credentials:


Email: {user.email}
Password: {otp_password}

Please log in at the portal and change your password for better security.

Thank you,
College Admin
"""
                try:
                    msg = MIMEText(message)
                    msg['Subject'] = subject
                    msg['From'] = 'alumniimentor@gmail.com'
                    msg['To'] = user.email

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('alumniimentor@gmail.com', 'lznjeuvbdpsozqim')
                    server.send_message(msg)
                    server.quit()
                except Exception as mail_error:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.exception('Error sending email while notifying')
                    messages.warning(request, "Alumni added but email failed to send.")

                messages.success(request, "Alumni added and login credentials sent via email.")
                return redirect(reverse('add_alumni1'))

            except Exception as e:
                traceback.print_exc()
                messages.error(request, f"Could not add alumni: {str(e)}")
        else:
            messages.error(request, "Form contains errors. Please correct them.")
    else:
        form = AlumniMembersForm(initial={'period_of_study': passing_year})

    return render(request,'alumniadmin_template/alumini_template.html',context={
        'form': form,
        'page_title': 'Add Alumni'
    })



def manage_alumni1(request):
    # ⚡ select_related('admin') fixes the blank name/email bug by pre-loading user fields
    alumini = Alumnimembers.objects.select_related('admin').all()
    form = AlumniMembersForm(request.POST or None, request.FILES or None)
    context = {
        'form' : form,
        'alumini': alumini,
        'page_title': 'Manage Alumni'
    }
    return render(request, 'alumniadmin_template/manage_alumini_template.html', context)


def edit_alumini(request, alumini_id):
    # Alumni object fetch (with related CustomUser)
    alumni = get_object_or_404(Alumnimembers, admin__id=alumini_id)
    user = alumni.admin  # Linked CustomUser

    form = AlumnimembersForm(request.POST or None, request.FILES or None, instance=alumni)

    context = {
        'form': form,
        'alumini_id': alumini_id,
        'page_title': 'Edit Alumni'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                # ✅ CustomUser update
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.gender = form.cleaned_data.get('gender')
                user.city = form.cleaned_data.get('city')
                user.state = form.cleaned_data.get('state')
                user.district_name = form.cleaned_data.get('district_name')
                user.country = form.cleaned_data.get('country')
                user.street_address = form.cleaned_data.get('street_address')
                user.date_of_birth = form.cleaned_data.get('date_of_birth')

                # Handle password update
                password = form.cleaned_data.get('password')
                if password:
                    user.set_password(password)

                user.save()
                if 'profile_pic' in request.FILES:
                    save_user_profile_pic(request.FILES['profile_pic'], user)

                # ✅ Alumnimembers update
                alumni.mobile = form.cleaned_data.get('mobile')
                alumni.current_street_address = form.cleaned_data.get('current_street_address')
                alumni.current_city = form.cleaned_data.get('current_city')
                alumni.current_district_name = form.cleaned_data.get('current_district_name')
                alumni.current_state = form.cleaned_data.get('current_state')
                alumni.course = form.cleaned_data.get('course')
                alumni.department = form.cleaned_data.get('department')
                alumni.period_of_study = form.cleaned_data.get('period_of_study')
                alumni.employment_status = form.cleaned_data.get('employment_status')
                alumni.employment_remarks = form.cleaned_data.get('employment_remarks')
                alumni.employment_sectors = form.cleaned_data.get('employment_sectors')
                alumni.course_studied = form.cleaned_data.get('course_studied')
                alumni.on_campus_achievements = form.cleaned_data.get('on_campus_achievements')
                alumni.beyond_college_achievements = form.cleaned_data.get('beyond_college_achievements')
                alumni.outside_institution_course = form.cleaned_data.get('outside_institution_course')
                alumni.contribution = form.cleaned_data.get('contribution')
                alumni.mode_of_payment = form.cleaned_data.get('mode_of_payment')
                alumni.membershipfees = form.cleaned_data.get('membershipfees')
                alumni.willingness = form.cleaned_data.get('willingness')
                alumni.is_active = form.cleaned_data.get('is_active')

                alumni.save()

                messages.success(request, "Successfully Updated Alumni")
                return redirect(reverse('alumni_admin_edit_alumini', args=[alumini_id]))

            except Exception as e:
                messages.error(request, "Could Not Update: " + str(e))
        else:
            messages.error(request, "Form contains errors, please check your inputs.")

    return render(request, 'alumniadmin_template/edit_alumini_template.html', context)


def deletealumini(request, alumini_id):
    alumini = get_object_or_404(CustomUser, id=alumini_id)
    delete_user_profile_pic(alumini)
    alumini.delete()

    messages.success(request, "Alumini deleted successfully!")
    return redirect(reverse('manage_alumni1'))

def fee_settings(request):
    form = FeeSettingsForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Fee Settings',
    }
    if request.method == 'POST':
        if form.is_valid():
            fee_name = form.cleaned_data.get('fee_name')
            fee_type = form.cleaned_data.get('fee_type')
            try:
               # Check for duplicates
                 if FeeSettings.objects.filter(fee_name=fee_name).exists():
                    messages.error(request, "Fee category with the same name already exists.")
                 else:
                    #Create and save the new fee category and type
                    feecategory = FeeSettings()
                    feecategory.fee_name = fee_name
                    feecategory.fee_type = fee_type
                    feecategory.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('fee_settings'))
            except Exception as e:
                messages.error(request, f"Could Not Add: {str(e)}")
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'alumniadmin_template/fee_settings_template.html', context)

def manage_fee_settings(request):
     form = FeeSettingsForm(request.POST or None)
     feesettings = FeeSettings.objects.all()
     context = {
        'feesettings': feesettings,
        'form': form,
        'page_title': 'Manage Fee Settings'
     }
     return render(request, "alumniadmin_template/manage_fee_settings_template.html",context)

def edit_fee_settings(request, fee_id):
    fee_settings = get_object_or_404(FeeSettings, id=fee_id)
    form = FeeSettingsForm(request.POST or None, instance=fee_settings)
    context = {
        'form': form,
        'page_title': 'Edit Fee Settings',
    }
    if request.method == 'POST':
        if form.is_valid():
            fee_name = form.cleaned_data.get('fee_name')
            fee_type = form.cleaned_data.get('fee_type')
            try:
                # Check for duplicates
                if FeeSettings.objects.filter(fee_name=fee_name).exclude(id=fee_id).exists():
                    messages.error(request, "Fee category with the same name already exists.")
                else:
                    # Update and save the fee category and type
                    fee_settings.fee_name = fee_name
                    fee_settings.fee_type = fee_type
                    fee_settings.save()
                    messages.success(request, "Successfully Updated")
                    return redirect(reverse('fee_settings'))
            except Exception as e:
                messages.error(request, f"Could Not Update: {str(e)}")
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'alumniadmin_template/edit_fee_settings_template.html', context)

def delete_fee_settings(request, fee_id):
    fee_settings = get_object_or_404(FeeSettings, id=fee_id)
    try:
        fee_settings.delete()
        messages.success(request, "Fee setting has been deleted")
    except Exception as e:
        messages.error(request, f"Could not delete fee setting: {str(e)}")
    return redirect(reverse('fee_settings'))
def add_fee_amount_settings(request):
    form = FeeAmountSettingsForm(request.POST or None)
    courses = Course.objects.all()
    feenames = FeeSettings.objects.values('fee_name').distinct()
    feetypes = FeeSettings.objects.values('fee_type').distinct()
    academic_year = Session.objects.all()
    
    context = {
        'form': form,
        'courses': courses,
        'feenames': feenames,
        'feetypes': feetypes,
        'academic_years':academic_year,
        'page_title': 'Fee Amount Settings',
    }
    
    return render(request, 'alumniadmin_template/add_fee_amount_settings_template.html', context)

@csrf_exempt
def get_feeamountsettings(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        feename = request.POST.get('feename')
        feetype = request.POST.get('feetype')
        amount = request.POST.get('amount')
        session_id = request.POST.get('session')

        try:
            course = Course.objects.get(id=course_id)
            session = Session.objects.get(id=session_id)

            fee_amount_setting = FeeAmountSettings(
                course=course,
                fee_name=feename,
                fee_type=feetype,
                amount=float(amount),
                session=session
            )
            fee_amount_setting.save()

            return JsonResponse({'success': True, 'message': 'Fee amount settings added successfully!'})

        except (Course.DoesNotExist, Session.DoesNotExist, ValueError) as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def manage_fee_amount_settings(request):
    fee_amount_settings = FeeAmountSettings.objects.all()
    context = {
        'fee_amount_settings': fee_amount_settings,
        'page_title': 'Manage Fee Amount Settings',
        }
    return render(request, 'alumniadmin_template/manage_fee_amount_template.html',context)

def edit_fee_amount(request):
    return render(request, 'alumniadmin_template/manage_fee_amount_template.html',)

@csrf_exempt
def alumni_students_list(request):
    query = request.POST.get("query", "").strip()
    # List to hold combined results
    results = []

        # Search in alumnimembers (joined with CustomUser)
    alumni = Alumnimembers.objects.select_related("admin","course").filter(
        Q(admin__first_name__icontains=query) |
        Q(admin__last_name__icontains=query) |
        Q(admin__profile_pic__icontains=query) |
        Q(mobile__icontains=query) |
        Q(course__name__icontains=query) |
        Q(department__department__icontains=query) |
        Q(current_street_address__icontains=query) |
        Q(current_city__icontains=query) |
        Q(current_district_name__icontains=query) |
        Q(current_state__icontains=query) |
        Q(period_of_study__icontains=query) |
        Q(admin__id__icontains=query)|
        Q(employment_status__icontains=query)|
        Q(employment_remarks__icontains=query)|
        Q(employment_sectors__icontains=query)
    ).values(
        "id", "mobile", "current_district_name", "current_state", "period_of_study", 
        "employment_status","employment_remarks","employment_sectors", "is_active","department__department", "course__name","admin__first_name", "admin__last_name", "admin__email","admin__id", "admin__profile_pic"
    )
    # Add alumni to results list
    for alumni in alumni:
        results.append({
            "id": alumni["id"],
            "name": f"{alumni['admin__first_name']} {alumni['admin__last_name']}",
            "email": alumni["admin__email"],
            "mobile": alumni["mobile"],
             "profile_pic":alumni["admin__profile_pic"],
             "course__name":alumni["course__name"],
             "department__department":alumni["department__department"],
            "district": alumni["current_district_name"],
            "status": alumni["employment_status"],
            "remarks": alumni["employment_remarks"],
            "sectors": alumni["employment_sectors"],
            "is_active": alumni["is_active"],
            "period_of_study":alumni["period_of_study"],
            "state":alumni["current_state"],
             "admin_id": alumni["admin__id"],
            "type": "Alumni"
        })

    # print("Response Data:", results)  # Debugging
    return JsonResponse(results, safe=False)

def edit_manage_alumini(request,alumini_id):
   # Fetch the alumni settings object using admin__id
    alumni = get_object_or_404(Alumnimembers, admin__id=alumini_id)
    user = alumni.admin  # Get the linked CustomUser object

    form = AlumnimembersForm(request.POST or None, request.FILES or None, instance=alumni)

    context = {
        'form': form,
        'alumini_id': alumini_id,
        'page_title': 'Edit Alumni'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                # Extract user details from the form
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic')

                # Update CustomUser fields
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.gender = gender
                

                if password:
                    user.set_password(password)  # Hash password

                user.save()  # Save changes to CustomUser
                if passport:
                    save_user_profile_pic(passport, user)

                # Update alumnimembers fields
                alumni.mobile = form.cleaned_data.get('mobile')
                alumni.current_street_address = form.cleaned_data.get('current_street_address')
                alumni.current_city = form.cleaned_data.get('current_city')
                alumni.current_district_name = form.cleaned_data.get('current_district_name')
                alumni.current_state = form.cleaned_data.get('current_state')
                alumni.course = form.cleaned_data.get('course')
                alumni.department = form.cleaned_data.get('department')
                alumni.period_of_study = form.cleaned_data.get('period_of_study')
                alumni.employment_status = form.cleaned_data.get('employment_status')
                alumni.employment_remarks = form.cleaned_data.get('employment_remarks')
                alumni.employment_sectors = form.cleaned_data.get('employment_sectors')
                alumni.is_active = form.cleaned_data.get('is_active')

                alumni.save()  # Save changes to alumnimembers

                messages.success(request, "Successfully Updated Alumni")
                return redirect(reverse('edit_manage_alumini', args=[alumini_id]))

            except Exception as e:
                messages.error(request, "Could Not Update: " + str(e))
        else:
            messages.error(request, "Form contains errors, please check your inputs.")
    return render(request, 'alumniadmin_template/edit_alumini_template.html', context) 

def alumniexcel_form(request):
      context = {
       
        'page_title': 'Download Alumni Form'
    }
      return render(request, 'alumniadmin_template/alumni_excelform_template.html', context) 

def alumniexceldata(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Alumni Data"

    headers = [
        "First Name", "Last Name","Gender","Phone Number", "Email","Period of Study",
         "Current Address","Employment Details","Membershipfees Details","Mode of Payment","Willingness to become an active member"
    ]

    # Write headers
    for col, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = Font(bold=True)

    # Set column widths
    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 20

    # Add validation for the pincode (last column, optional)
    pincode_dv = DataValidation(type="whole", operator="greaterThan", formula1=0)
    pincode_dv.error = 'Please enter a valid pincode'
    pincode_dv.errorTitle = 'Invalid Pincode'
    sheet.add_data_validation(pincode_dv)
    pincode_dv.add('K2:K1048576')  # Assuming Pincode is column 11 (K)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=alumni_data_form.xlsx'
    workbook.save(response)
    return response


def upload_alumni_excel(request):
    if request.method == 'POST':
        form = AluminiExcelForm(request.POST, request.FILES)
        if form.is_valid():
            if 'excel_form' not in request.FILES:
                messages.error(request, "Please upload a valid Excel file.")
                return redirect('upload_alumni_data')

            excel_file = request.FILES['excel_form']
            try:
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb.active

                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    try:
                        row = list(row)
                        row.extend([None] * (12 - len(row)))  # Ensure length
                        (
                            first_name, last_name, gender, mobile, email, period_of_study,
                            current_street_address, employment_remarks, contribution,
                            membershipfees, mode_of_payment, willingness
                        ) = row[:12]

                        required_fields = [first_name, last_name, gender, mobile, email, period_of_study, current_street_address]
                        if any(field in (None, "") for field in required_fields):
                            messages.warning(request, f"Skipping row due to missing required fields: {row}")
                            continue

                        # Create CustomUser (OTP will be auto-generated in save())
                        user1 = CustomUser(
                            first_name=first_name,
                            last_name=last_name,
                            gender=gender,
                            email=email,
                            user_type=5  # Alumni
                        )
                        user1.save()  # triggers OTP generation
                        otp_password = user1.otp  # get the generated OTP

                        # Now set this OTP as the password
                        user1.set_password(otp_password)
                        user1.save()

                        # Create or update Alumnimembers
                        alumni, created = Alumnimembers.objects.update_or_create(
                            admin=user1,
                            defaults={
                                "mobile": mobile,
                                "current_street_address": current_street_address,
                                "period_of_study": period_of_study,
                                "employment_remarks": employment_remarks,
                                "contribution": contribution,
                                "membershipfees": membershipfees,
                                "mode_of_payment": mode_of_payment,
                                "willingness": willingness,
                                "is_active": True,
                            }
                        )

                        # Prepare email content
                        subject = "Your Alumni Login Details"
                        message = f"""
Dear {first_name} {last_name},

Your alumni account has been successfully created.

Here are your login credentials:

Email: {email}
Password: {otp_password}

Please login to the portal and change your password for security.

Thank you,
Alumni Management Team
"""

                        # Send email using smtplib
                        try:
                            msg = MIMEText(message)
                            msg['Subject'] = subject
                            msg['From'] = 'alumniimentor@gmail.com'
                            msg['To'] = email

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.ehlo()
                            server.starttls()
                            server.login('alumniimentor@gmail.com', 'lznjeuvbdpsozqim')  # replace with your Gmail App Password
                            server.send_message(msg)
                            server.quit()
                        except Exception as mail_error:
                            import logging
                            logger = logging.getLogger(__name__)
                            logger.exception('Error sending email while notifying alumni')
                            messages.warning(request, f"Alumni {email} added but email failed to send.")

                        messages.success(request, f"Alumni data for {first_name} uploaded successfully!")

                    except Exception as e:
                        traceback.print_exc()
                        messages.error(request, f"Unexpected error: {e}. Skipping row.")

                return redirect('/alumini/upload_alumni_data')

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('upload_alumni_data')

    else:
        form = AluminiExcelForm()
    return render(request, 'alumniadmin_template/alumini_upload_template.html', {'form': form})



def alumni_print(request):
    course = Course.objects.all()
    
    # 🔄 Dynamically generate passing years (Current Year down to 2000)
    current_year = datetime.now().year
    passing_years = list(range(current_year, 1999, -1)) 
    school = School.objects.first()
    context = {
        'course': course,
        'school': school,
        'passing_years': passing_years,  # 👈 Clear context variable name
        'page_title': 'Alumni List'
    }
    return render(request, 'alumniadmin_template/alumni_print_template.html', context)



@csrf_exempt
def alumni_search_list(request):
    if request.method == 'POST':
        course = request.POST.get('course', '').strip()
        emp_sec = request.POST.get('emp_sec', '').strip()
        name = request.POST.get('name', '').strip()
        emp_status = request.POST.get('emp_status', '').strip()
        period_of_study = request.POST.get('period_of_study', '').strip()

        try:
            # 1. Initialize the base queryset targeting the Alumnimembers model
            queryset = Alumnimembers.objects.all()

            # 2. Build filters safely using standard object field lookups
            if course:
                queryset = queryset.filter(course__name__iexact=course)

            if emp_sec:
                queryset = queryset.filter(employment_sectors__icontains=emp_sec)

            if emp_status:
                queryset = queryset.filter(employment_status__icontains=emp_status)

            if period_of_study:
                queryset = queryset.filter(period_of_study__icontains=period_of_study)

            if name:
                queryset = queryset.filter(admin__first_name__istartswith=name)

            # 3. Optimize database hits by fetching foreign keys upfront
            alumni_records = queryset.select_related('admin', 'course', 'department')

            # 4. Construct the JSON response dictionary array explicitly from object properties
            results = []
            for a in alumni_records:
                # Handle potential null values for relations safely
                course_title = a.course.name if a.course else "N/A"
                dept_title = a.department.name if a.department else "N/A"
                
                # Format first name & last name gracefully depending on availability
                first = a.admin.first_name if a.admin else ""
                last = a.admin.last_name if a.admin else ""
                full_name = f"{first}.{last}".strip(".") if (first or last) else "Unknown"

                results.append({
                    "id": a.id,
                    "name": full_name,
                    "email": a.admin.email if a.admin else "N/A",
                    "mobile": a.mobile,
                    "course": course_title,
                    "department": dept_title,
                    "district": a.current_district_name,
                    "state": a.current_state,
                    "status": a.employment_status,
                    "is_active": a.is_active,
                    "period_of_study": a.period_of_study,
                    "employment_sectors": a.employment_sectors,
                    "admin_id": a.admin.id if a.admin else None,
                })

            return JsonResponse(results, safe=False)

        except Exception as e:
            # This returns the raw system error text to your browser alert window
            return JsonResponse({"error": f"Backend Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


# @csrf_exempt
# def alumni_search_list(request):
#     if request.method == 'POST':
#         course = request.POST.get('course', '').strip()
#         emp_sec = request.POST.get('emp_sec', '').strip()
#         name = request.POST.get('name', '').strip()
#         emp_status = request.POST.get('emp_status', '').strip()
#         period_of_study = request.POST.get('period_of_study', '').strip()

#         try:
#             filters = Q()

#             if course:
#                 try:
#                     course_obj = Course.objects.get(name__iexact=course)
#                     filters &= Q(course=course_obj)
#                 except Course.DoesNotExist:
#                     return JsonResponse({"error": f"Course '{course}' not found."}, status=404)

#             if emp_sec:
#                 filters &= Q(employment_sectors__icontains=emp_sec)

#             if emp_status:
#                 filters &= Q(employment_status__icontains=emp_status)

#             if period_of_study:
#                 filters &= Q(period_of_study__icontains=period_of_study)

#             if name:
#                 filters &= Q(admin__first_name__istartswith=name)

#             alumni = Alumnimembers.objects.filter(filters).values(
#                 "id", "mobile", "current_district_name", "current_state", "period_of_study",
#                 "employment_status", "employment_sectors", "is_active",
#                 "department__department", "course__name",
#                 "admin__first_name", "admin__last_name", "admin__email", "admin__id"
#             )

#             results = []
#             for a in alumni:
#                 results.append({
#                     "id": a["id"],
#                     "name": f"{a['admin__first_name']}.{a['admin__last_name']}",
#                     "email": a["admin__email"],
#                     "mobile": a["mobile"],
#                     "course": a["course__name"],
#                     "department": a["department__name"],
#                     "district": a["current_district_name"],
#                     "state": a["current_state"],
#                     "status": a["employment_status"],
#                     "is_active": a["is_active"],
#                     "period_of_study": a["period_of_study"],
#                     "employment_sectors": a["employment_sectors"],
#                     "admin_id": a["admin__id"],
#                 })

#             return JsonResponse(results, safe=False)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request method."}, status=405)

# def download_db_backup(request):
    # Set credentials from settings or environment variables
    # db_user = os.environ.get("MYSQL_USER", "root")
    # db_password = os.environ.get("MYSQL_PASSWORD", "")
    # db_name = os.environ.get("MYSQL_DB", "new_clgimentor")
    # db_host = "localhost"  # Change if needed

    # now = datetime.now().strftime("%Y%m%d_%H%M%S")
    # backup_filename = f"db_backup_{now}.sql"
    # backup_path = os.path.join(settings.BASE_DIR, backup_filename)

    # try:
    #     # Generate the MySQL dump
    #     dump_cmd = [
    #         "mysqldump",
    #         "-u", db_user,
    #         f"-p{db_password}",
    #         "-h", db_host,
    #         db_name
    #     ]
    #     print(dump_cmd)
    #     # Create the backup file
    #     with open(backup_path, "w") as f:
    #         subprocess.run(dump_cmd, stdout=f, check=True)

    #     # Serve the backup file as a download response
    #     return FileResponse(open(backup_path, 'rb'), as_attachment=True, filename=backup_filename)

    # except subprocess.CalledProcessError:
    #     raise Http404("Backup failed. Check database credentials or permissions.")
    # except FileNotFoundError:
    #     raise Http404("Backup file not found.")

# def download_db_backup(request):
#     if not request.user.is_staff:
#         return HttpResponse("Unauthorized", status=401)

#     # Create in-memory stream
#     backup_io = StringIO()
#     call_command('dumpdata', format='json', stdout=backup_io)

#     # Prepare response
#     backup_io.seek(0)
#     response = HttpResponse(backup_io.read(), content_type='application/json')
#     filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response

def add_jobpostings1(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            designation = form.cleaned_data.get('designation')
            employer=form.cleaned_data.get('employer')
            location=form.cleaned_data.get('location')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image = fs.url(filename)
        
            jobposting = CareerInfo()
            jobposting.designation = designation
            jobposting.employer = employer
            jobposting.location = location
            jobposting.description = description
            image = request.FILES.get('image')
            jobposting.image = image
            jobposting.save()
            messages.success(request, "New Job Posting added successfully.")
            return redirect(reverse('add_jobpostings1'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full")
    else:
        form = JobPostingForm()

    context = {
        'form': form,
        'page_title': 'Add Job Postings'
    }
    return render(request, 'alumniadmin_template/placement_cell_template.html',context)

def  manage_jobpostings1(request):
 career = CareerInfo.objects.all()
 context = {
        'career': career,
        'page_title': 'Manage  Job Postings'
    }
 return render(request, 'alumniadmin_template/manage_jobpostings.html',context ) 

def editjobpostings(request,jobposting_id):
    instance = get_object_or_404(CareerInfo, id=jobposting_id)
    form = JobPostingForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'school_id': jobposting_id,
        'page_title': 'Edit Job Postings'
    }
    if request.method == 'POST':
        if form.is_valid():

            designation = form.cleaned_data.get('designation')
            employer=form.cleaned_data.get('employer')
            location=form.cleaned_data.get('location')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            
            try:
                    jobposting = CareerInfo.objects.get(id=jobposting_id)
                    jobposting.designation = designation
                    jobposting.employer = employer
                    jobposting.location = location
                    jobposting.description = description
                    image = request.FILES.get('image')
                    if image:
                        # Save the new image
                        fs = FileSystemStorage()
                        filename = fs.save(image.name, image)
                        jobposting.image = image  # Assign the new image
                    else:
                        # Keep the existing image (do nothing)
                        messages.info(request, "No new image selected. Retaining the existing image.")

                    jobposting.save()    
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_jobpostings.html',context )  

def deletejobpostings(request,jobposting_id):
    jobposting = get_object_or_404(CareerInfo, id=jobposting_id)
    jobposting.delete()
    messages.success(request, "Job Posting deleted successfully!")
    return redirect(reverse('manage_jobpostings1'))

def add_companies1(request):
    if request.method == 'POST':
        form = AssociatedCompaniesForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            website=form.cleaned_data.get('website')
            contact=form.cleaned_data.get('contact')
            company_overview=form.cleaned_data.get('company_overview')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image = fs.url(filename)
        
            companies = AssociatedCompanies()
            companies.company_name = company_name
            companies.website = website
            companies.contact = contact
            companies.company_overview = company_overview
            image = request.FILES.get('image')
            companies.image = image
            companies.save()
            messages.success(request, "New Associated Company added successfully.")
            return redirect(reverse('add_companies1'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
            form = AssociatedCompaniesForm()

    context = {
        'form': form,
        'page_title': 'Add Associated Companies'
    }
    return render(request, 'alumniadmin_template/associated_companies_template.html',context)

def  manage_companies1(request):
 company = AssociatedCompanies.objects.all()
 context = {
        'company': company,
        'page_title': 'Manage Associated Company Details'
    }
 return render(request, 'alumniadmin_template/manage_companies.html',context ) 

def editcompany(request,company_id):
    instance = get_object_or_404(AssociatedCompanies, id=company_id)
    form = AssociatedCompaniesForm(request.POST or None,request.FILES or None, instance=instance)
    context = {
        'form': form,
        'school_id': company_id,
        'page_title': 'Edit Associated Company Details'
    }
    if request.method == 'POST':
        if form.is_valid():

            company_name = form.cleaned_data.get('company_name')
            website=form.cleaned_data.get('website')
            contact=form.cleaned_data.get('contact')
            company_overview=form.cleaned_data.get('company_overview')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name,image)
            
            try:
                    company = AssociatedCompanies.objects.get(id=company_id)
                    company.company_name = company_name
                    company.website = website
                    company.contact = contact
                    company.company_overview = company_overview
                    company.image = image
                    company.save()    
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_company.html',context ) 

def deletecompany(request,company_id):
    company = get_object_or_404(AssociatedCompanies, id=company_id)
    company.delete()
    messages.success(request, "Associated Company details has been deleted successfully!")
    return redirect(reverse('manage_companies1'))

def add_alumni_events1(request):
    if request.method == 'POST':
        form = AlumniEventsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            event_name = form.cleaned_data.get('event_name')
            event_date = form.cleaned_data.get('event_date')
            event_type = form.cleaned_data.get('event_type')
            event_venue = form.cleaned_data.get('event_venue')
            event_status = form.cleaned_data.get('event_status')
            department = form.cleaned_data.get('department')
            course = form.cleaned_data.get('course')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image = fs.url(filename)
        
            events = AlumniEventsInfo()
            events.event_name = event_name
            events.event_date = event_date
            events.event_type = event_type
            events.event_venue = event_venue
            events.event_status = event_status
            events.department = department
            events.course = course
            events.description = description
            image = request.FILES.get('image')
            events.image = image
            events.save()
            messages.success(request, "New Alumni Event added successfully.")
            return redirect(reverse('add_alumni_events1'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = AlumniEventsForm()

    context = {
        'form': form,
        'page_title': 'Add Alumni Events'
    }
    return render(request, 'alumniadmin_template/add_alumni_events_template.html',context)

def  manage_alumnievents1(request):
 event = AlumniEventsInfo.objects.all()
 context = {
        'event': event,
        'page_title': 'Manage  Alumni Events'
    }
 return render(request, 'alumniadmin_template/manage_alumni_events.html',context )

def edit_alumnievents(request,event_id):
    instance = get_object_or_404(AlumniEventsInfo, id=event_id)
    form = AlumniEventsForm(request.POST or None,request.FILES or None, instance=instance)
    context = {
        'form': form,
        'school_id': event_id,
        'page_title': 'Edit Alumni Events'
    }
    if request.method == 'POST':
        if form.is_valid():

            event_name = form.cleaned_data.get('event_name')
            event_date = form.cleaned_data.get('event_date')
            event_type = form.cleaned_data.get('event_type')
            event_venue = form.cleaned_data.get('event_venue')
            event_status = form.cleaned_data.get('event_status')
            department = form.cleaned_data.get('department')
            course = form.cleaned_data.get('course')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name,image)
            
            
            
            try:
                    event = AlumniEventsInfo.objects.get(id=event_id)
                    event.event_name = event_name
                    event.event_date = event_date
                    event.event_type = event_type
                    event.event_venue = event_venue
                    event.event_status = event_status
                    event.department = department
                    event.course = course
                    event.description = description
                    event.image = image
                    event.save()    
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_alumni_events.html',context ) 

def deletealumnievents(request,event_id):
    event = get_object_or_404(AlumniEventsInfo, id=event_id)
    event.delete()
    messages.success(request, "Alumni Event Information is deleted successfully!")
    return redirect(reverse('manage_alumnievents1')) 

def add_careerguidanceprogrammes1(request):
    if request.method == 'POST':
        form = CareerGuidanceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            programme_name = form.cleaned_data.get('programme_name')
            programme_date = form.cleaned_data.get('programme_date')
            programme_type = form.cleaned_data.get('programme_type')
            programme_venue = form.cleaned_data.get('programme_venue')
            programme_status = form.cleaned_data.get('programme_status')
            department = form.cleaned_data.get('department')
            course = form.cleaned_data.get('course')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image = fs.url(filename)
        
            programmes = CareerGuidance()
            programmes.programme_name = programme_name
            programmes.programme_date = programme_date
            programmes.programme_type = programme_type
            programmes.programme_venue = programme_venue
            programmes.programme_status = programme_status
            programmes.department = department
            programmes.course = course
            programmes.description = description
            image = request.FILES.get('image')
            programmes.image = image
            programmes.save()
            messages.success(request, "New Career Guidance Programme added successfully.")
            return redirect(reverse('add_careerguidanceprogrammes1'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = CareerGuidanceForm()

    context = {
        'form': form,
        'page_title': 'Add Career Guidance Programme Details'
    }
    return render(request, 'alumniadmin_template/add_career_guidance_programme_template.html',context)

def  manage_careerguidanceprogrammes1(request):
 programme = CareerGuidance.objects.all()
 context = {
        'programme': programme,
        'page_title': 'Manage  Career Guidance Programme Details'
    }
 return render(request, 'alumniadmin_template/manage_career_guidance_programme_template.html',context )

def guidecareer(request,programme_id):
    instance = get_object_or_404(CareerGuidance, id=programme_id)
    form = CareerGuidanceForm(request.POST or None,request.FILES or None, instance=instance)
    context = {
        'form': form,
        'school_id': programme_id,
        'page_title': 'Edit Career Guidance Programme Details'
    }
    if request.method == 'POST':
        if form.is_valid():
            programme_name = form.cleaned_data.get('programme_name')
            programme_date = form.cleaned_data.get('programme_date')
            programme_type = form.cleaned_data.get('programme_type')
            programme_venue = form.cleaned_data.get('programme_venue')
            programme_status = form.cleaned_data.get('programme_status')
            department = form.cleaned_data.get('department')
            course = form.cleaned_data.get('course')
            description=form.cleaned_data.get('description')
            image=form.cleaned_data.get('image')
            fs = FileSystemStorage()
            filename = fs.save(image.name,image)
            
            
            
            try:
                    programmes = CareerGuidance.objects.get(id=programme_id)
                    programmes.programme_name = programme_name
                    programmes.programme_date = programme_date
                    programmes.programme_type = programme_type
                    programmes.programme_venue = programme_venue
                    programmes.programme_status = programme_status
                    programmes.department = department
                    programmes.course = course
                    programmes.description = description
                    image = request.FILES.get('image')
                    programmes.image = image
                    programmes.save()
   
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'alumniadmin_template/edit_career_guidance_template.html',context ) 

def delete_career(request,programme_id):
    programme = get_object_or_404(CareerGuidance, id=programme_id)
    programme.delete()
    messages.success(request, "Career Guidance Programme details deleted successfully!")
    return redirect(reverse('manage_careerguidanceprogrammes1')) 


@login_required
@user_passes_test(lambda u: u.user_type == '1')  # Assuming '1' is for HOD/Admin
def create_alumni_chatgroup1(request):
    if request.method == 'POST':
        form = ChatGroupForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            period_of_study = form.cleaned_data['period_of_study']

            # Check if such group already exists
            if ChatGroup.objects.filter(course=course, period_of_study=period_of_study).exists():
                messages.error(request, "A chat group with this Course and Period of Study already exists.")
            else:
                chat_group = form.save()

                # Add current admin as group member
                GroupMembership.objects.create(
                    chat_group=chat_group,
                    user=request.user,
                    is_admin=True
                )

                messages.success(request, "Chat group created and you're added as Group Admin.")
                return redirect('create_alumni_chatgroup1')
    else:
        form = ChatGroupForm()

    return render(request, 'alumniadmin_template/create_alumni_chatgroup.html', {
        'form': form,
        'page_title': 'Create Alumni Chat Group'
    })



@login_required
@user_passes_test(is_admin)
def manage_alumni_chatgroup1(request):
    groups = ChatGroup.objects.all().order_by('-created_at')  
    context = {
        'groups': groups,
        'page_title': 'Manage Alumni Chat Groups',
    }
    return render(request, 'hod_template/manage_alumni_groupchats.html', context)


@login_required
@user_passes_test(is_admin)
def delete_chat_group(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    group.delete()
    messages.success(request, 'Chat group deleted successfully.')
    return redirect('manage_alumni_groupchats')




@login_required
@user_passes_test(lambda u: u.user_type == '1')  # Assuming '1' is HOD/Admin
def add_member_to_group(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            period = form.cleaned_data['period_of_study']

            # Get the group based on course and period_of_study
            group = ChatGroup.objects.filter(course=course, period_of_study=period).first()
            if not group:
                messages.error(request, "Group does not exist.")
                return redirect('add_member_to_group')

            # Get alumni with matching course and period_of_study
            alumni_list = Alumnimembers.objects.filter(
                course=course,
                period_of_study=period
            )

            # Get existing group members' user IDs
            group_members = GroupMembership.objects.filter(
                chat_group=group
            ).values_list('user_id', flat=True)

            # Handle individual alumnus addition via ID
            if request.POST.get('add_id'):
                alumnus = get_object_or_404(Alumnimembers, id=request.POST.get('add_id'))

                GroupMembership.objects.get_or_create(
                    chat_group=group,
                    user=alumnus.admin
                )
                messages.success(request, f"New Alumni {alumnus.admin.first_name} added to the group.")

                return redirect('add_member_to_group')

            # Show template to select alumni
            return render(request, 'hod_template/select_alumni.html', {
                'alumni_list': alumni_list,
                'group': group,
                'group_members': group_members,
                'page_title': "Select Alumni for Chat-Group"
            })

    else:
        form = AddMemberForm()

    return render(request, 'hod_template/add_member_to_group.html', {
        'form': form,
        'page_title': 'Add Alumni to Group Chat'
    })


@login_required
@user_passes_test(lambda u: u.user_type == '1')  # Only admin
def adminview_group_chat(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    messages_in_group = group.messages.all().order_by('timestamp')

    # Get all members from GroupMembership model
    group_memberships = GroupMembership.objects.filter(chat_group=group).select_related('user')

    context = {
        'group': group,
        'chat_history': messages_in_group,
        'group_memberships': group_memberships,
        'page_title': f"Group Chat - {group.course.name} ({group.period_of_study})",
    }
    return render(request, 'hod_template/adminview_group_chat.html', context)

@login_required
@user_passes_test(lambda u: u.user_type == '1')
def admin_delete_group_message(request, message_id):
    message = get_object_or_404(GroupChatMessage, id=message_id)
    group_id = message.chat_group.id
    message.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('adminview_group_chat', group_id=group_id)

@login_required
@user_passes_test(lambda u: u.user_type == '1')
def remove_member_from_group(request, group_id, user_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    user = get_object_or_404(CustomUser, id=user_id)
    membership = GroupMembership.objects.filter(chat_group=group, user=user).first()
    if membership:
        membership.delete()
        messages.success(request, f"{user.first_name} removed from group.")
    else:
        messages.warning(request, "Member not found in this group.")
    return redirect('adminview_group_chat', group_id=group_id)




def download_db_backup(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    # Get DB settings
    db_settings = settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_host = db_settings['HOST'] or 'localhost'

    # File name
    filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    # Run mysqldump command
    try:
        result = subprocess.run(
            [
                "mysqldump",
                f"-u{db_user}",
                f"-p{db_password}",
                f"-h{db_host}",
                db_name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Backup failed: {e.stderr.decode()}", status=500)

    # Return SQL file as response
    response = HttpResponse(result.stdout, content_type='application/sql')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def viewalumnifeedback(request):
    feedback = AlumniFeedback.objects.all()
    import logging
    logger = logging.getLogger(__name__)
    logger.debug('feedback: %s', feedback)
    context = {
        'feedbacks' : feedback
    }
    return render(request,"alumniadmin_template/view_alumni_feedback.html",context)

@login_required
def reply_feedback(request, feedback_id):
    logger.debug('feedback_id: %s', feedback_id)
    if request.method == 'POST':
        try:
            feedback = AlumniFeedback.objects.get(id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return JsonResponse({'status': 'success', 'reply': reply}, status=200)
        except AlumniFeedback.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Feedback not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)




