from datetime import timezone
import json
import random
import smtplib
from io import BytesIO
from email.mime.text import MIMEText
from multiprocessing import context
import requests
from django.conf import settings
import openpyxl
import logging
from django.db.models.functions import Cast
import os 
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Concat, Replace, Upper
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.conf import settings
import random
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.shortcuts import render
from openpyxl import load_workbook
from .models import Student
# from .forms import AccAdminForm
from .models import CustomUser
from .forms import *
from .models import *
import pandas as pd
import os
from django.db.models import Q
from django.views.decorators.http import require_POST
import traceback
from collections import defaultdict
import traceback
from django.db import transaction
import re
from django.template.loader import render_to_string
# from weasyprint import HTML, CSS  # Commented out due to missing GTK+ libraries on Windows
from datetime import date
from .models import Session
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image, ImageOps
from weasyprint import HTML, CSS
logger = logging.getLogger(__name__)
def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = Subjectmaster.objects.all().count()
    total_course = Course.objects.values('name').distinct().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    modulesettings = ModuleSettings.objects.all()
    # print("Modulesettings:", modulesettings)
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        # subject_list.append(subject.subject.name[:7])
        attendance_list.append(attendance_count)
      

         
    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'modulesettings':modulesettings
       
    }
    return render(request, 'hod_template/home_content.html', context)


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
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=None, date_of_birth=date_of_birth)
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
                if passport:
                    save_user_profile_pic(passport, user)
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {
        'form': student_form,
        'page_title': 'Add Student Profile'
    }

    if request.method == "POST":

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
            district_name = student_form.cleaned_data.get('district_name')
            street_address = student_form.cleaned_data.get('street_address')
            state = student_form.cleaned_data.get('state')
            country = student_form.cleaned_data.get('country')

            parent_name = student_form.cleaned_data.get('parent_name')
            guardian_contact_number = student_form.cleaned_data.get('guardian_contact_number')
            mother_name = student_form.cleaned_data.get('mother_name')
            blood_group = student_form.cleaned_data.get('blood_group')
            mother_tongue = student_form.cleaned_data.get('mother_tongue')
            caste = student_form.cleaned_data.get('caste')
            religion = student_form.cleaned_data.get('religion')
            aadhar_number = student_form.cleaned_data.get('aadhar_number')
            school_house = student_form.cleaned_data.get('school_house')
            bus_stop = student_form.cleaned_data.get('bus_stop')
            bus_number = student_form.cleaned_data.get('bus_number')
            allergies_medical_conditions = student_form.cleaned_data.get('allergies_medical_conditions')
            alternate_contact_number = student_form.cleaned_data.get('alternate_contact_number')
            date_of_birth = student_form.cleaned_data.get('date_of_birth')

            # Profile picture is optional
            passport = request.FILES.get('profile_pic')

            try:

                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    user_type=3,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=None,
                    date_of_birth=date_of_birth,
                )

                user.gender = gender
                user.street_address = street_address
                user.city = city
                user.state = state
                user.district_name = district_name
                user.country = country
                user.save()

                if passport:
                    save_user_profile_pic(passport, user)

                student = user.student
                student.session = session
                student.course = course
                student.admission_number = admission_number
                student.parent_name = parent_name
                student.guardian_contact_number = guardian_contact_number
                student.mother_name = mother_name
                student.blood_group = blood_group
                student.mother_tongue = mother_tongue
                student.date_of_birth = date_of_birth
                student.caste = caste
                student.religion = religion
                student.aadhar_number = aadhar_number
                student.school_house = school_house
                student.bus_stop = bus_stop
                student.bus_number = bus_number
                student.allergies_medical_conditions = allergies_medical_conditions
                student.alternate_contact_number = alternate_contact_number

                student.save()

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))

            except Exception as e:
                messages.error(request, "Could Not Add : " + str(e))

        else:
            messages.error(request, "Please correct the errors in the form.")

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
            password = accadmin_form.cleaned_data.get('new_password')
            gender = accadmin_form.cleaned_data.get('gender')
            date_of_birth=accadmin_form.cleaned_data['date_of_birth']
            passport = request.FILES.get('profile_pic')
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password,country=country,city=city,date_of_birth=date_of_birth,district_name=district_name,street_address=street_address, user_type=4,state=state, gender=gender, first_name=first_name, last_name=last_name, profile_pic=None)
                user.save()
                if passport:
                    save_user_profile_pic(passport, user)
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_acc_admin'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")

    return render(request, 'hod_template/add_acc_admin_template.html', context)



def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course & Division'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            division = form.cleaned_data.get('division')
            try:
                # Check for duplicates
                if Course.objects.filter(name=name, division=division).exists():
                    messages.error(request, "Course with the same name and division already exists.")
                else:
                    # Create and save the new course
                    course = Course()
                    course.name = name
                    course.division = division
                    course.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('add_course'))
            except Exception as e:
                messages.error(request, f"Could Not Add: {str(e)}")
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_course_template.html', context)


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

    return render(request, 'hod_template/add_subject_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Teacher'
    }
    return render(request, "hod_template/manage_staff.html", context)

def manage_acc_admin(request):
    allacademicAdmin = CustomUser.objects.filter(user_type=4)
   
    context = {
        'allacademicAdmin': allacademicAdmin,
        'page_title': 'Manage Academic Admin'
    }
    return render(request, "hod_template/manage_acc_admin.html", context)


def manage_student(request):

    session = Session.objects.filter(is_active=True).first()
    students = CustomUser.objects.filter(
    user_type=3,
    student__session=session
).exclude(
    student__course__name="QUALIFIERS",
).annotate(
    class_order=Cast("student__course__name", IntegerField()),
    gender_order=Case(
        When(gender='M', then=Value(1)),
        When(gender='F', then=Value(2)),
        When(gender='O', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
).order_by(
    "class_order",                 # Numeric class order
    "student__course__division",   # A, B, C...
    "gender_order",                # M -> F -> O
    "first_name",
    "last_name"
)

    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    return render(request, "hod_template/manage_student.html", context)


def manage_course(request):
    courses = Course.objects.all()
    message = request.GET.get('message', '')
    message_type = request.GET.get('message_type', '')
    context = {
        'courses': courses,
        'page_title': 'Manage Course & Division',
        'message': message,
        'message_type': message_type
    }
    return render(request, "hod_template/manage_course.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subject Assign'
    }
    return render(request, "hod_template/manage_subject.html", context)


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
            passport = request.FILES.get('profile_pic')
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
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
                if passport:
                    save_user_profile_pic(passport, user)
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fulfill all the requirements")
    else:
        # user = CustomUser.objects.get(id=staff_id)
        # print("User:", user)
        staff = Staff.objects.get(id=staff_id)
      
        return render(request, "hod_template/edit_staff_template.html", context)    

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
                if passport:
                    save_user_profile_pic(passport, user)
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fill out the form properly!")
            return render(request, "hod_template/edit_student_template.html", context)
            # messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_student_template.html", context)

def students_list(request):
    query = request.GET.get("q", "").strip()
    session = Session.objects.filter(is_active=True).first()
    students = CustomUser.objects.filter(user_type="3", student__session=session).annotate(

        # Full Name
        full_name=Upper(
            Concat(
                "first_name",
                Value(" "),
                "last_name"
            )
        ),

        # Course Search (10A, 10 A, 10-A)
        course_search=Upper(
            Replace(
                Concat(
                    "student__course__name",
                    "student__course__division"
                ),
                Value(" "),
                Value("")
            )
        ),

        # Gender Order
        gender_order=Case(
            When(gender="M", then=Value(1)),
            When(gender="F", then=Value(2)),
            When(gender="O", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    )

    if query:

        gender_query = query.upper() if query.upper() in ["M", "F", "O"] else None

        normalized_query = (
            query.upper()
                 .replace(" ", "")
                 .replace("-", "")
        )

        filters = (
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(city__icontains=query) |
            Q(district_name__icontains=query) |
            Q(student__course__name__icontains=query) |
            Q(student__course__division__icontains=query) |
            Q(course_search__icontains=normalized_query)
        )

        if gender_query:
            filters |= Q(gender__iexact=gender_query)

        students = students.filter(filters).distinct()

    # Sorting:
    # 1. Class
    # 2. Division
    # 3. Male -> Female -> Others
    # 4. First Name
    # 5. Last Name
    students = students.order_by(
        "student__course__name",
        "student__course__division",
        "gender_order",
        "first_name",
        "last_name"
    )

    context = {
        "page_title": "Students List",
        "students": students,
    }

    return render(request, "hod_template/students_list_template.html", context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': course_id,
        'page_title': 'Edit Course & Division'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            division = form.cleaned_data.get('division')
            try:
                if  Course.objects.filter(name=name, division=division).exists():
                    messages.error(request, "Course with the same name and division already exists.")
                else:
                    course = Course.objects.get(id=course_id)
                    course.name = name
                    course.division = division
                    course.save()
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_course_template.html', context)


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
    return render(request, 'hod_template/edit_subject_template.html', context)


def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Academmic Year'}
    # if request.method == 'POST':
    #     if form.is_valid():
    #         try:
    #             form.save()
    #             messages.success(request, "New Academic Year Created")
    #             return redirect(reverse('add_session'))
    #         except Exception as e:
    #             messages.error(request, 'Could Not Add ' + str(e))
    #     else:
    #         messages.error(request, 'Fill Form Properly ')
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():

           
            Session.objects.filter(is_active=True).update(
                is_active=False
            )

           
            session = form.save(commit=False)
            session.is_active = True
            session.save()

            return redirect('add_session')

    else:
        form = SessionForm()
    return render(request, "hod_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Academic Year'}
    return render(request, "hod_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)

    context = {
        'form': form,
        'session_id': session_id,
        'page_title': 'Edit Academic Year'
    }

    if request.method == "POST":

        if form.is_valid():

            today = date.today()

            start_date = form.cleaned_data["start_year"]
            end_date = form.cleaned_data["end_year"]
            is_active = form.cleaned_data["is_active"]

            # Current Academic Year മാത്രമേ Active ആക്കാൻ പാടുള്ളൂ
            if is_active and not (start_date <= today <= end_date):
                messages.error(
                    request,
                    "Only the current Academic Year can be set as Active."
                )
                return render(
                    request,
                    "hod_template/edit_session_template.html",
                    context
                )

            try:

                if is_active:
                    Session.objects.exclude(id=instance.id).update(is_active=False)

                form.save()

                messages.success(request, "Academic Year Updated")
                return redirect(reverse("edit_session", args=[session_id]))

            except Exception as e:
                messages.error(request, str(e))

        else:
            messages.error(request, "Invalid Form Submitted")

    return render(request, "hod_template/edit_session_template.html", context)

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
        return render(request, 'hod_template/staff_feedback_template.html', context)
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
        return render(request, "hod_template/staff_leave_view.html", context)
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
        return render(request, "hod_template/student_leave_view.html", context)
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

    return render(request, "hod_template/admin_view_attendance.html", context)


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

def admin_view_profile(request):    # Get the currently logged-in admin object
    admin = get_object_or_404(Admin, admin=request.user)
       # Bind form with request data and existing admin instance
    form = AdminEditForm(request.POST or None, request.FILES or None, instance=admin)

    # For rendering
    context = {
        'form': form,
        'page_title': 'View/Edit Profile'
    }

    if request.method == 'POST':
        try:
            if form.is_valid():

                # Extract form fields
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                # Get the related CustomUser object
                custom_user = admin.admin

                # Set password if provided
                if password:
                    custom_user.set_password(password)

                # Update user names
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()

                # Handle profile image if provided
                if passport:
                    save_user_profile_pic(passport, custom_user)

                # Save the Admin model changes
                form.save()

                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))

            else:
                messages.error(request, "Invalid Data Provided")

        except Exception as e:
            messages.error(request, "Error Occurred While Updating Profile: " + str(e))

    return render(request, "hod_template/admin_view_profile.html", context)

def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


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
                'title': "Student Management System",
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
    delete_user_profile_pic(staff)
    staff.delete()
    messages.success(request, "Teacher deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    delete_user_profile_pic(student)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Student.objects.filter(course=course).exists():
        messages.error(request, "This course cannot be deleted as it has associated students.")
        return redirect(reverse('manage_course'))
    else:
        course.delete()
        messages.success(request, "Successfully Deleted")
        return redirect(reverse('manage_course'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('manage_subject'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    try:
        with transaction.atomic():

            # Active session delete ചെയ്യുകയാണെങ്കിൽ
            if session.is_active:

                # Delete ചെയ്യുന്ന session ഒഴികെയുള്ള sessions
                other_sessions = Session.objects.exclude(id=session.id)

                if other_sessions.exists():

                    # Previous session ആദ്യം നോക്കുക
                    new_active = other_sessions.filter(
                        id__lt=session.id
                    ).order_by("-id").first()

                    # Previous ഇല്ലെങ്കിൽ Next session
                    if not new_active:
                        new_active = other_sessions.filter(
                            id__gt=session.id
                        ).order_by("id").first()

                    if new_active:
                        # എല്ലാ sessions-ഉം inactive ആക്കുക
                        Session.objects.update(is_active=False)

                        # പുതിയ active session
                        new_active.is_active = True
                        new_active.save()

            # ഇനി delete ചെയ്യുക
            session.delete()

        messages.success(request, "Academic Year deleted successfully.")

    except Exception:
        messages.error(
            request,
            "There are students assigned to this session. Please move them to another session."
        )

    return redirect(reverse("manage_session"))






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
    return render(request, 'hod_template/add_student_template.html', context)
def add_school(request):
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
                messages.error(request, "School already exists.")
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
                messages.success(request, "School successfully added.")
                return redirect(reverse('add_school'))
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = SchoolForm()

    context = {
        'form': form,
        'page_title': 'Add School'
    }
    return render(request, 'hod_template/add_school_template.html', context)

def  manage_school(request):
 school = School.objects.all()
 context = {
        'school': school,
        'page_title': 'Manage  School'
    }
 return render(request, 'hod_template/manage_school_template.html',context )   

def edit_school(request,school_id):
    instance = get_object_or_404(School, id=school_id)
    form = SchoolForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'school_id': school_id,
        'page_title': 'Edit School'
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
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)
                    image=filename
                    # image = fs.url(filename)
                    school.image = image
                    school.save()
                    messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_school_template.html',context ) 
def delete_school(request, school_id):
    school = get_object_or_404(School, id=school_id)
    school.delete()
    messages.success(request, "School deleted successfully!")
    return redirect(reverse('manage_school'))


def add_alumini(request):
    if request.method == 'POST':
        form = AlumniMembersForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data

                passport = request.FILES.get('profile_pic')

                otp_password = str(random.randint(100000, 999999))

                # Check if email already exists
                if CustomUser.objects.filter(email=data['email']).exists():
                    messages.error(request, "User with this email already exists.")
                    return redirect(reverse('add_alumini'))

                # Create user
                user = CustomUser.objects.create_user(
                    email=data['email'],
                    password=otp_password,
                    user_type='8',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
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
                return redirect(reverse('add_alumini'))

            except Exception as e:
                traceback.print_exc()
                messages.error(request, f"Could not add alumni: {str(e)}")
        else:
            messages.error(request, "Form contains errors. Please correct them.")
    else:
        form = AlumniMembersForm()

    return render(request, 'hod_template/alumini_template.html', {
        'form': form,
        'page_title': 'Add Alumni'
    })

def manage_alumini(request):
    alumini = CustomUser.objects.filter(user_type=8).exclude(
        Q(first_name__isnull=True) | Q(first_name__exact="") |
        Q(last_name__isnull=True) | Q(last_name__exact="")
    )
    form = AlumniMembersForm(request.POST or None,request.FILES or None)
    context = {
        'form' : form,
        'alumini': alumini,
        'page_title': 'Manage Alumni'
    }
    return render(request,'hod_template/manage_alumini_template.html',context)



@csrf_exempt
def approve_alumini(request):
    if request.method == "POST":
        alumni_id = request.POST.get("id")
        try:
            alumni = Alumnimembers.objects.get(id=alumni_id)
            alumni.is_active = True
            alumni.save()
            return JsonResponse({"status": "success"})
        except alumni.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Alumni not found"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
def edit_alumini(request, alumini_id):
    alumni = get_object_or_404(
        Alumnimembers,
        admin__id=alumini_id
    )

    user = alumni.admin

    # Save original email
    original_email = user.email

    # Initial data from user fields
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'gender': user.gender,
        'date_of_birth': user.date_of_birth,
        'street_address': user.street_address,
        'city': user.city,
        'district_name': user.district_name,
        'state': user.state,
        'country': user.country,
    }

    form = AlumniMembersForm(
        request.POST or None,
        request.FILES or None,
        instance=alumni,
        initial=initial_data
    )

    context = {
        'form': form,
        'alumini_id': alumini_id,
        'page_title': 'Edit Alumni'
    }

    if request.method == 'POST':

        if form.is_valid():

            try:

                # =========================================================
                # GET FORM DATA
                # =========================================================

                new_email = form.cleaned_data.get('email')

                # =========================================================
                # UPDATE USER DETAILS
                # =========================================================

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = new_email

                user.gender = form.cleaned_data.get('gender')
                user.date_of_birth = form.cleaned_data.get('date_of_birth')

                user.street_address = form.cleaned_data.get('street_address')
                user.city = form.cleaned_data.get('city')
                user.district_name = form.cleaned_data.get('district_name')
                user.state = form.cleaned_data.get('state')
                user.country = form.cleaned_data.get('country')

                user.course = form.cleaned_data.get('course')
                user.mobile = form.cleaned_data.get('mobile')

                user.current_street_address = form.cleaned_data.get(
                    'current_street_address'
                )
                user.current_city = form.cleaned_data.get(
                    'current_city'
                )
                user.current_district_name = form.cleaned_data.get(
                    'current_district_name'
                )
                user.current_state = form.cleaned_data.get(
                    'current_state'
                )
                user.current_course = form.cleaned_data.get(
                    'current_course'
                )
                user.current_department = form.cleaned_data.get(
                    'current_department'
                )
                user.current_period_of_study = form.cleaned_data.get(
                    'current_period_of_study'
                )

                user.employment_status = form.cleaned_data.get(
                    'employment_status'
                )
                user.employment_remarks = form.cleaned_data.get(
                    'employment_remarks'
                )

                # =========================================================
                # PASSWORD
                # =========================================================

                password = form.cleaned_data.get('password')

                if password:
                    user.set_password(password)

                # =========================================================
                # SAVE USER & PROFILE IMAGE
                # =========================================================

                user.save()
                passport = request.FILES.get('profile_pic')
                if passport:
                    save_user_profile_pic(passport, user)

                # =========================================================
                # UPDATE ALUMNI DETAILS
                # =========================================================

                alumni.mobile = form.cleaned_data.get('mobile')

                alumni.current_street_address = form.cleaned_data.get(
                    'current_street_address'
                )
                alumni.current_city = form.cleaned_data.get(
                    'current_city'
                )
                alumni.current_district_name = form.cleaned_data.get(
                    'current_district_name'
                )
                alumni.current_state = form.cleaned_data.get(
                    'current_state'
                )

                alumni.course = form.cleaned_data.get('course')
                alumni.department = form.cleaned_data.get(
                    'department'
                )
                alumni.period_of_study = form.cleaned_data.get(
                    'period_of_study'
                )

                alumni.employment_status = form.cleaned_data.get(
                    'employment_status'
                )
                alumni.employment_remarks = form.cleaned_data.get(
                    'employment_remarks'
                )

                alumni.employment_sectors = form.cleaned_data.get(
                    'employment_sectors'
                )

                alumni.course_studied = form.cleaned_data.get(
                    'course_studied'
                )

                alumni.on_campus_achievements = form.cleaned_data.get(
                    'on_campus_achievements'
                )

                alumni.beyond_college_achievements = form.cleaned_data.get(
                    'beyond_college_achievements'
                )

                alumni.outside_institution_course = form.cleaned_data.get(
                    'outside_institution_course'
                )

                alumni.contribution = form.cleaned_data.get(
                    'contribution'
                )

                alumni.mode_of_payment = form.cleaned_data.get(
                    'mode_of_payment'
                )

                alumni.membershipfees = form.cleaned_data.get(
                    'membershipfees'
                )

                alumni.willingness = form.cleaned_data.get(
                    'willingness'
                )

                alumni.is_active = form.cleaned_data.get(
                    'is_active'
                )

                # Save alumni
                alumni.save()

                # =========================================================
                # EMAIL CHANGE NOTIFICATION
                # =========================================================

                if original_email != new_email:

                    subject = "Your Alumni Email Has Been Updated"

                    message = f"""
Dear {user.first_name} {user.last_name},

Your email associated with your alumni account has been successfully updated.

Updated Email: {new_email}

If this change was not made by you, please contact the administrator immediately.

Thank you,
College Admin
"""

                    try:

                        msg = MIMEText(message)

                        msg['Subject'] = subject
                        msg['From'] = 'alumniimentor@gmail.com'
                        msg['To'] = new_email

                        server = smtplib.SMTP(
                            'smtp.gmail.com',
                            587
                        )

                        server.ehlo()
                        server.starttls()

                        server.login(
                            'alumniimentor@gmail.com',
                            'YOUR_GMAIL_APP_PASSWORD'
                        )

                        server.send_message(msg)
                        server.quit()

                    except Exception as mail_error:

                        import logging

                        logger = logging.getLogger(__name__)

                        logger.exception(
                            'Error sending update email'
                        )

                        messages.warning(
                            request,
                            "Alumni updated, but email notification failed."
                        )

                # =========================================================
                # SUCCESS
                # =========================================================

                messages.success(
                    request,
                    "Alumni profile updated successfully."
                )

                return redirect(
                    reverse(
                        'edit_alumini',
                        args=[alumini_id]
                    )
                )

            except Exception as e:

                messages.error(
                    request,
                    "Could not update alumni: " + str(e)
                )

        else:

            messages.error(
                request,
                "Form contains errors. Please correct them."
            )

    return render(
        request,
        'hod_template/edit_alumini_template.html',
        context
    )

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
        # Q(department__department__icontains=query) |
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
        "employment_status","employment_remarks","employment_sectors", "is_active", "course__name","admin__first_name", "admin__last_name", "admin__email","admin__id", "admin__profile_pic", "mode_of_payment"
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
            #  "department__department":alumni["department__department"],
            "district": alumni["current_district_name"],
            "mode_of_payment": alumni.get("mode_of_payment", ""),
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

def delete_alumini(request, alumini_id):
    alumini = get_object_or_404(CustomUser, id=alumini_id)
    delete_user_profile_pic(alumini)
    alumini.delete()

    messages.success(request, "Alumini deleted successfully!")
    return redirect(reverse('manage_alumini'))


# def delete_alumini(request, alumini_id):
#     print("llll")
#     alumini = get_object_or_404(Alumnimembers, id=alumini_id)
#     print(alumini,"kkk")
#     alumini.delete()
#     messages.success(request, "Alumini deleted successfully!")
#     return redirect(reverse('manage_alumini'))

def upload_alumni_data(request):
    if request.method == 'POST':
        form = AluminiExcelForm(request.POST, request.FILES)
        if form.is_valid():
            if 'excel_form' not in request.FILES:
                messages.error(request, "Please upload a valid Excel file.")
                return redirect('/alumini/upload_alumni')

            excel_file = request.FILES['excel_form']
            try:
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb.active
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    try:
                        # Ensure row has exactly 16 values, filling missing ones with None
                        # row = list(row)  # Convert tuple to list
                        # row.extend([None] * (16 - len(row)))  # Fill missing values with None

                        (studentname, email, mobile, gender, course_studied, period_of_study, permanent_locality, permanent_district, permanent_state, 
                                           current_locality, current_district, current_state,current_status) = row
                        # Check for required fields
                        required_fields = [studentname, email, mobile, gender, course_studied, period_of_study, permanent_locality, permanent_district, permanent_state, 
                                           current_locality, current_district, current_state,current_status]
                        
                        if any(field is None or field == "" for field in required_fields):
                            messages.warning(request, f"Skipping row due to missing values: {row}")
                            continue
                        
                        # Validate mobile number
                        if not isinstance(mobile, (int, str)) or len(str(mobile)) != 10:
                            messages.warning(request, f"Invalid mobile number {mobile}. Skipping row.")
                            continue
                        
                        # same_as_permanent = bool(same_as_permanent) if same_as_permanent is not None else False
                        # is_active = bool(is_active) if is_active is not None else False
                        
                        Alumnimembers.objects.create(
                            studentname=studentname,
                            # image=image if image else None,
                            gender=gender,
                            email=email,
                            mobile=str(mobile),
                            course_studied=course_studied,
                            period_of_study=period_of_study,
                            current_status=current_status,
                            permanent_locality=permanent_locality,
                            permanent_district=permanent_district,
                            permanent_state=permanent_state,
                            current_locality=current_locality,
                            current_district=current_district,
                            current_state=current_state,
                        )
                        messages.success(request, f"Alumni data for {studentname} uploaded successfully!")
                    except ValidationError as e:
                        messages.error(request, f"Validation error: {e}. Skipping row.")
                    
                    except Exception as e:
                        print(e)
                        messages.error(request, f"Unexpected error: {e}. Skipping row.")

                return redirect('/alumini/upload_alumni')
            
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('/alumini/upload_alumni')
    
    else:
        form = AluminiExcelForm()

    return render(request, 'hod_template/alumini_upload_template.html', {'form': form})

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
    return render(request, 'hod_template/fee_settings_template.html', context)

def manage_fee_settings(request):
     form = FeeSettingsForm(request.POST or None)
     feesettings = FeeSettings.objects.all()
     context = {
        'feesettings': feesettings,
        'form': form,
        'page_title': 'Manage Fee Settings'
     }
     return render(request, "hod_template/manage_fee_settings_template.html",context)

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
    return render(request, 'hod_template/edit_fee_settings_template.html', context)

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
    
    return render(request, 'hod_template/add_fee_amount_settings_template.html', context)

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
    return render(request, 'hod_template/manage_fee_amount_template.html',context)

def edit_fee_amount(request, fee_id):
    instance = get_object_or_404(FeeAmountSettings, id=fee_id)
    form = FeeAmountSettingsForm(request.POST or None,request.FILES or None,instance=instance)

    for field in ['session', 'course', 'fee_name', 'fee_type']:
        if field in form.fields:
            form.fields[field].disabled = True

    context = {
        'form' : form,
        'fee_id': fee_id,
        'page_title': 'Edit Fee Amount'
    }
    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            try:
                fee = FeeAmountSettings.objects.get(id=fee_id)
                fee.amount = amount
                fee.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_fee_amount', args=[fee_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Could Not Update")
    return render(request,'hod_template/edit_fee_amount.html',context)


def delete_fee_amount(request, fee_id):
    fee_amount = get_object_or_404(FeeAmountSettings, id=fee_id)
    fee_amount.delete()
    messages.success(request, "Fee Amount deleted successfully!")
    return redirect(reverse('manage_fee_amount_settings'))

def get_email_by_name(request):
    name = request.GET.get('name', '').strip()
    # user = CustomUser.objects.all().count()

    if name:
        return JsonResponse({'email': name + "@gmail.com"})
    else:
        return JsonResponse({'email': ''})



def view_filtered_class_results_by_subject(request):
    courses = Course.objects.all()
    selected_course_id = request.GET.get('course')
    selected_subject_id = request.GET.get('subject')

    subjects = Subject.objects.filter(course__id=selected_course_id) if selected_course_id else Subject.objects.none()
    students = Student.objects.filter(course__id=selected_course_id) if selected_course_id else Student.objects.none()

    student_results = []
    if selected_course_id and selected_subject_id:
        results = StudentResult.objects.filter(
            student__in=students,
            subject__id=selected_subject_id
        ).order_by('term')

        # Group by student and term
        result_dict = {}

        for res in results:
            key = res.student.id
            term = res.term

            if key not in result_dict:
                result_dict[key] = {
                    'student': res.student,
                    'subject': res.subject,
                    'terms': {}  # To hold term-1, term-2, etc.
                }

            exam_name = res.exam_type.exam_name.lower()
            if term not in result_dict[key]['terms']:
                result_dict[key]['terms'][term] = {
                    'tp': None,
                    'pt': None,
                    'semester': None,
                    'remarks': ''
                }

            if 'tp' in exam_name:
                result_dict[key]['terms'][term]['tp'] = res.test
            elif 'pt' in exam_name:
                result_dict[key]['terms'][term]['pt'] = res.exam
            elif 'semester' in exam_name:
                result_dict[key]['terms'][term]['semester'] = res.semester

            result_dict[key]['terms'][term]['remarks'] = res.remarks

        student_results = list(result_dict.values())

    context = {
        'courses': courses,
        'subjects': subjects,
        'results': student_results,
        'selected_course_id': selected_course_id,
        'selected_subject_id': selected_subject_id,
        'page_title': 'Class Result (Subject-Wise)'
    }
    return render(request, "hod_template/class_wise_result_subject.html", context)

def edit_allAdmin(request, allAdmin):
    accadmin_user = get_object_or_404(CustomUser, id=allAdmin)

    if request.method == 'POST':
        form = AccAdminForm(request.POST, request.FILES, instance=accadmin_user)
        if form.is_valid():
            admin = form.save(commit=False)

            # Update individual fields if needed
            admin.first_name = form.cleaned_data.get('first_name')
            admin.last_name = form.cleaned_data.get('last_name')
            admin.city = form.cleaned_data.get('city')
            admin.district_name = form.cleaned_data.get('district_name')
            admin.street_address = form.cleaned_data.get('street_address')
            admin.state = form.cleaned_data.get('state')
            admin.country = form.cleaned_data.get('country')
            admin.email = form.cleaned_data.get('email')
            admin.gender = form.cleaned_data.get('gender')
            admin.date_of_birth = form.cleaned_data.get('date_of_birth')

            # Handle new password
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                admin.set_password(new_password)

            admin.save()
            if 'profile_pic' in request.FILES:
                save_user_profile_pic(request.FILES['profile_pic'], admin)

            messages.success(request, "Profile updated successfully!")
            return redirect(reverse('edit_allAdmin', kwargs={'allAdmin': allAdmin}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccAdminForm(instance=accadmin_user)

    context = {
        'form': form,
        'id': allAdmin,
        'page_title': 'Edit Profile'
    }
    return render(request, 'hod_template/edit_accAdmin.html', context)
def delete_allAdmin(request, allAdmin):
    accadmin_user = get_object_or_404(CustomUser, id=allAdmin)
    delete_user_profile_pic(accadmin_user)
    accadmin_user.delete()
    messages.success(request, "Academic Admin deleted successfully!")
    return redirect(reverse('manage_alumni_admin'))

def admin_studentgraph(request):
    courses = Course.objects.all() 
    Sessions = get_object_or_404(Session, is_active=True)
    context ={
        "page_title":"Student Graphwise",
         "courses":courses,
         "sessions": Sessions
    }
    return render(request, "hod_template/studentgraph.html", context)
def get_student_marks(request):
#     student_id = request.GET.get('student_id')
#     subject_id = request.GET.get('subject_id')
#     course_id = request.GET.get('course_id')

#     try:
#         subject = Subject.objects.get(subject_id=subject_id, course_id=course_id)
#     except Subject.DoesNotExist:
#         return JsonResponse({"results": []})

#     results = StudentResult.objects.filter(
#         student_id=student_id,
#         subject_id=subject.id
#     ).select_related('exam_type')

#     def sort_key(item):
#         name = item.exam_type.exam_name.upper()
#         if name.startswith('TP'):
#             return (1, int(name[2:] or 0))
#         elif name.startswith('PT'):
#             return (2, int(name[2:] or 0))
#         elif 'SEMESTER' in name:
#             return (3, int(name.replace('SEMESTER', '') or 0))
#         return (4, 0)

#     results = sorted(results, key=sort_key)

#     # Build dynamic result list with exam_type_id
#     data_list = []
#     for result in results:
#         exam_name = result.exam_type.exam_name
#         upper_exam = exam_name.upper()

#         marks = None
#         raw = None
#         if upper_exam.startswith("TP"):
#             raw = result.test
#         elif upper_exam.startswith("PT"):
#             raw = result.test
#         elif "SEMESTER" in upper_exam:
#             raw = result.test

#         if raw not in [None, '']:
#             try:
#                 marks = float(raw)
#             except ValueError:
#                 marks = None

#         data_list.append({
#     "exam_name": exam_name,
#     "marks": marks,
#     "exam_type": result.exam_type.id,
#     "exam_type_name": result.exam_type.exam_name  # <-- add this
# })

#     return JsonResponse({"results": data_list})
    student_id = request.GET.get('student_id')
    subject_id = request.GET.get('subject_id')
    course_id = request.GET.get('course_id')
    sessions = request.GET.get('session_id')

    subject = Subject.objects.get(subject_id=subject_id, course_id=course_id)

    results = StudentResult.objects.filter(
        student_id=student_id,
        subject_id=subject.id,
        session_id=sessions
    ).select_related('exam_type')

    # ✅ ORDER HERE
    def sort_key(r):
        exam = r.exam_type

        exam_type = exam.exam_type.upper().strip()  # TP / PT / Semester
        term = exam.term or ""

        num = ''.join(filter(str.isdigit, term))
        term_number = int(num) if num else 0

        return (exam_type, term_number)

    results = sorted(results, key=sort_key)

    data_list = []

    for r in results:
        raw = r.test
        try:
            marks = float(raw) if raw not in [None, ''] else None
        except:
            marks = None

        data_list.append({
            "exam_name": r.exam_type.exam_name,
            "exam_type": r.exam_type.exam_type,
            "term": r.exam_type.term,
            "marks": marks
        })

    return JsonResponse({"results": data_list})

def get_subjects(request):
    course_id = request.POST.get('course')
    
    # Fetch all subjects linked to the course
    subject_qs = Subject.objects.filter(course_id=course_id)

    # Get only unique subject names (and one instance per name)
    unique_subjects = {}
    for subject in subject_qs:
        if subject.subject.name not in unique_subjects:
            unique_subjects[subject.subject.name] = subject

    subject_data_value = []
    for subject in unique_subjects.values():
        subject_data_value.append({
            "id": subject.id,
            "name": subject.subject.name
        })

    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)
def staff_bulk_student_data1(request):
    course = request.POST.get('course')
    subject_data1 = request.POST.get('subject')
    term_wise = request.POST.get('term')
    exam_name = request.POST.get('exam')
    session = request.POST.get('session')
    try:
        course_obj = get_object_or_404(Course, id=course)
        subject_obj = get_object_or_404(Subject, id=subject_data1)
        examtype_obj = get_object_or_404(ExamtypeSettings, id=exam_name)
        session_obj = get_object_or_404(Session, id=session)
        results=StudentResult.objects.filter(
    subject_id=subject_obj.id,
    term=term_wise,
    exam_type_id=examtype_obj.id,
    student__course_id=course_obj.id,
    session_id=session_obj.id
   
)
        # print(results)
        bulk_data_list = []
        for r in results:
                data = {
                "student_id": r.id,
                "student_name": f"{r.student.admin.first_name} {r.student.admin.last_name}",
                "admission_number": r.student.admission_number,
                "subject_id": r.subject.id,
                "term": r.term,
                "exam_type_id": r.exam_type.id,
                "exam_type_name": r.exam_type.exam_name.lower(),  # ADD THIS LINE
                "test": r.test,
                "remarks": r.remarks,
                # "session": r.session

}
                bulk_data_list.append(data)

        return JsonResponse(bulk_data_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_course_list(request):
    course_id = request.POST.get('course')
    
    # Fetch all subjects linked to the course
    subject_qs = Subject.objects.filter(course_id=course_id)

    # Get only unique subject names (and one instance per name)
    unique_subjects = {}
    for subject in subject_qs:
        if subject.subject.name not in unique_subjects:
            unique_subjects[subject.subject.name] = subject

    subject_data_value = []
    for subject in unique_subjects.values():
        subject_data_value.append({
            "id": subject.id,
            "name": subject.subject.name
        })

    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)


@csrf_exempt
def view_filtered_class_results(request):
    courses = Course.objects.all()
    terms = ExamtypeSettings.objects.values_list('term', flat=True).distinct()
    selected_course = ''
    selected_term = ''
    selected_exam = ''
    selected_exam_name = ''
    exam_type_id = '' 
    sessions = Session.objects.filter(is_active=True).first()
    # sessions = Session.objects.all().order_by("-start_year")
    selected_session = request.GET.get("session", "")
    selected_course = selected_term = selected_exam = selected_exam_name = ''
    student_data = defaultdict(lambda: {
        "marks": {},
        "percentage": 0,
        "name": ""
    })
    all_subjects = set()
    results = []

    if request.GET.get("course") and request.GET.get("term") and request.GET.get("exam") and request.GET.get("session"):
        course_id = request.GET.get("course")
        term = request.GET.get("term")
        exam_type_id = request.GET.get("exam")
        session_id = request.GET.get("session")

        selected_course = course_id
        selected_term = term
        selected_exam = exam_type_id
        try:
            exam_obj = ExamtypeSettings.objects.get(id=selected_exam)
            selected_exam_name = exam_obj.exam_name
        except ExamtypeSettings.DoesNotExist:
            selected_exam_name = ''

        student_qs = Student.objects.filter(course_id=course_id)
        student_ids = student_qs.values_list('id', flat=True)

        results = StudentResult.objects.filter(
            student_id__in=student_ids,
            exam_type_id=exam_type_id,
            term=term,
            session_id=session_id
        ).select_related('student', 'subject', 'exam_type','session')
        print("filtered results:",results)

        # 👉 Load max_marks once from ExamtypeSettings (assuming same for all subjects in this exam)
        try:
            max_marks = ExamtypeSettings.objects.get(id=exam_type_id).max_marks
        except ExamtypeSettings.DoesNotExist:
            max_marks = 20  # fallback

        for row in results:
            full_name = f"{row.student.admin.first_name} . {row.student.admin.last_name}"
            subject_name = row.subject.subject.name
            all_subjects.add(subject_name)

            mark = row.test or row.exam or row.semester

            student_data[row.student.id]["name"] = full_name
            student_data[row.student.id]["marks"][subject_name] = mark

        # 🔢 Percentage calculation using actual max_marks from ExamtypeSettings
        for student in student_data.values():
            total_obtained = 0
            total_max = 0

            for subject, mark in student["marks"].items():
                try:
                    mark = float(mark)
                    total_obtained += mark
                    total_max += max_marks  # each subject has same max in this exam
                except (ValueError, TypeError):
                    continue

            percentage = (total_obtained / total_max) * 100 if total_max else 0
            student["percentage"] = round(percentage, 2)
          
    # 📦 Context return
    context_data = {
        'courses': courses,
        'terms': terms,
        'student_subject_marks': student_data.values(),
        'subjects': sorted(all_subjects),
        'selected_course': selected_course,
        'selected_term': selected_term,
        'selected_exam': selected_exam_name,
        'examname': exam_type_id,
        'page_title': "Class Wise Result",
        'sessions': sessions,
        'results': results
    }
    return render(request, 'hod_template/class_wise_result.html', context_data)

   
EXAM_COLUMNS = [
    'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7', 'TP8', 'TP9', 'TP10', 'TP11', 'TP12',
    'PT1', 'PT2', 'PT3',
    'SEMESTER1', 'SEMESTER2'
]

def subject_class_result(request):

  
    courses = Course.objects.all()
    subjects = Subject.objects.none()
    selected_course = request.GET.get('course')
    selected_subject = request.GET.get('subject')
    all_data = []
    sessions = Session.objects.filter(is_active=True).first()

    exam_columns = []

    if selected_course:
        subjects = Subject.objects.filter(course_id=selected_course)
        
#         subjects = Subjectmaster.objects.filter(
#     subject__course_id=selected_course
# ).distinct()
        
        if selected_subject:
            selected_subject = int(selected_subject)
            students = Student.objects.filter(course_id=selected_course)

            # ✅ Fetch dynamic exam names
            exam_columns_qs = ExamtypeSettings.objects.all().order_by('id')
            exam_columns = [e.exam_name.strip().upper() for e in exam_columns_qs]

            results_qs = StudentResult.objects.filter(
                student__in=students,
                subject__id=selected_subject,
                session__is_active=True
            ).select_related('student__admin', 'exam_type', 'session')

            data = {}

            for student in students:
                data[student.id] = {
                    'student': student,
                    **{col: None for col in exam_columns}
                }

            for result in results_qs:
                exam_name = result.exam_type.exam_name.strip().upper()
                student_id = result.student.id
                data_field = result.test or result.exam or result.semester

                if exam_name in exam_columns:
                    data[student_id][exam_name] = data_field

            for student_data in data.values():
                all_data.append({
                    'student': student_data['student'],
                    'marks': {k: v for k, v in student_data.items() if k != 'student'}
                })

    context = {
        'courses': courses,
        'subjects': subjects,
        'selected_course': selected_course,
        'selected_subject': selected_subject,
        'exam_columns': exam_columns,
        'all_data': all_data,
        'page_title': "Subjectwise Result",
        'sessions': sessions
    }

    return render(request, 'hod_template/classwise_result.html', context)
def get_student(request):
    course_id = request.POST.get('course')

    try:
        course = get_object_or_404(Course, id=course_id)
        students = Student.objects.filter(course_id=course)

        student_data = []
        for student in students:
            student_data.append({
                "id": student.id,
                "name": student.admin.first_name + " " + student.admin.last_name  # Admin model use cheyyunnu enn assumption
            })

        return JsonResponse(student_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def admin_bulk_result_new(request):
    #  qs = Course.objects.values('id','name', 'division').distinct()
    #  class_list = [f"{item['name']} {item['division']}" for item in qs]
    #  print(class_list)
     course = Course.objects.all()
     examnames = ExamtypeSettings.objects.all()
     sessions = Session.objects.filter(
        is_active=True
    ).first()
     context = {
          'courses': course,
          'examnames': examnames,
          'sessions': sessions,
           'page_title': 'Result Bulk Upload',
     }
     return render(request, 'hod_template/result_bulk_upload_template.html', context)          
def new_student_result(request): 
     courses = Course.objects.all()
     context = {
            'courses': courses,
        #   'examnames': examnames,
            'page_title': 'Student Wise Result',
     }

     return render(request, 'hod_template/new_studentwise_result.html', context)

def extract_number(value):
    if isinstance(value, str):
        match = re.search(r'\d+', value)
        if match:
            return int(match.group())
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
@csrf_exempt
@require_POST
def save_student_results_new1(request):
   
    try:
        data = json.loads(request.body)
        created_count = 0
        updated_count = 0
        failed = []

        for entry in data:
            try:
                student_id = entry.get('student_id')
                subject_id = entry.get('subject_id')
                test_score = entry.get('test', 0)
                exam_score = entry.get('exam', 0)
                session_id = entry.get('session')
                semester_score = entry.get('semester', 0)
                remarks = entry.get('remarks', '').strip()
                term = entry.get('term', '').strip().title()
                exam_type_code = entry.get('exam_type')  # PT1, PT2, TP1 etc.
                course_id = entry.get('course')
                # print(session_id,"session_id")
                # print(f"\nProcessing entry: {entry}")
                # print(f"Extracted IDs - Student: {student_id}, Subject: {subject_id}, Course: {course_id}, Exam Type: {exam_type_code}")

                # Validate required fields
                if not all([student_id, subject_id, term, exam_type_code, course_id, session_id]):
                    failed.append(f"Missing required fields in entry: {entry}")
                    continue

                # Skip fully empty rows
                if test_score == 0 and exam_score == 0 and semester_score == 0 and not remarks:
                    print("Skipped:", student_id)
                    continue

                # Convert scores to float
                try:
                    test_score = float(test_score)
                    exam_score = float(exam_score)
                    semester_score = float(semester_score)
                except ValueError:
                    failed.append(f"Invalid score value in entry: {entry}")
                    continue

                # Count non-zero scores
                score_fields_filled = sum([
                    1 if test_score > 0 else 0,
                    1 if exam_score > 0 else 0,
                    1 if semester_score > 0 else 0
                ])

                if score_fields_filled == 0 and not remarks:
                    remarks = "Absent"
                elif score_fields_filled > 1:
                    failed.append(f"Multiple scores provided for student {student_id}. Only one score allowed.")
                    continue

                # Get related objects
                # print(f"Fetching Student ID: {student_id}")
                student = get_object_or_404(Student, id=student_id)
                # print(f"Found student: {student}")

                # print(f"Fetching Subject ID: {subject_id}, Course ID: {course_id}")
                subject = get_object_or_404(Subject, id=subject_id, course_id=course_id)
                # print(f"Found subject: {subject}")

                # Fetching ExamtypeSettings using exam_name, not exam_type
                # print(f"Fetching Exam Type with exam_name: {exam_type_code}")
                try:
                    exam = ExamtypeSettings.objects.get(exam_name__iexact=exam_type_code)
                except ExamtypeSettings.DoesNotExist:
                    failed.append(f"Exam name '{exam_type_code}' not found.")
                    print(f"Exam name '{exam_type_code}' not found.")
                    continue

                print(f"Found exam type: {exam}")

                subjectmaster = subject.subject  # Adjust if named differently in your model

                # Save result
                result, created = StudentResult.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam_type=exam,  # This is correct now
                    term=term,
                    session_id=session_id,
                    defaults={
                        'subjectmaster': subjectmaster,
                        'test': test_score,
                        'exam': exam_score,
                        'semester': semester_score,
                        'remarks': remarks or "Absent"
                    }
                )
                print(result)
                if created:
                    print(f"Created new result for student {student}")
                    created_count += 1
                else:
                    print(f"Updated result for student {student}")
                    updated_count += 1

            except Exception as entry_exception:
                print(f"Exception while processing entry for student {entry.get('student_id')}: {entry_exception}")
                print(traceback.format_exc())
                failed.append(f"Error in entry {entry}: {entry_exception}")
                continue

        # Response
        total = created_count + updated_count
        if total == 0:
            status = "empty"
            message = "No results saved."
        else:
            status = "success"
            message = f"{created_count} created, {updated_count} updated."

        print(f"Total created: {created_count}, updated: {updated_count}")
        print(f"Failed entries: {failed}")

        return JsonResponse({
            "status": status,
            "message": message,
            "failures": failed
        })

    except Exception as e:
        print("Unhandled exception in save_student_results:")
        print(traceback.format_exc())
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
@csrf_exempt
def get_students_bulk1(request):
    
    course = request.POST.get('course')
    subject_data_value1 = request.POST.get('subject_data_value1')
    session = request.POST.get('session')
    try:
         course = get_object_or_404(Course, id=course)
         subject_data_value = get_object_or_404(Subject, id=subject_data_value1)
#          students_with_subjects = Student.objects.filter(
#                 course_id=course,
#                  course_id__in=Subject.objects.filter(course_id=course, subject=subject_data_value.subject).values_list('course_id', flat=True)
# ) 
         students_with_subjects = (
    Student.objects.filter(course=course, session=session)
    .select_related("admin")
    .annotate(
        gender_order=Case(
            When(admin__gender="M", then=Value(1)),
            When(admin__gender="F", then=Value(2)),
            When(admin__gender="O", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    )
    .order_by(
        "gender_order",
        "admin__first_name",
        "admin__last_name"
    )
)
         bulk_data_list = []
         for students in students_with_subjects:
           data = {
                         "id": students.id,
                         "name": students.admin.first_name + " " + students.admin.last_name,
                         "admission_number": students.admission_number
                    }
           bulk_data_list.append(data)
           print("Bulk data list:", bulk_data_list)  # Debugging line
         return JsonResponse(json.dumps(bulk_data_list),content_type='application/json', safe=False)
    except Exception as e:
     return JsonResponse({"error": str(e)}, status=400)
    
def get_term_list(request):
    exam_name = request.POST.get('exam_name')
    examtype = ExamtypeSettings.objects.get(id=exam_name)
    term_list = examtype.term.split(",")  # Assuming CSV string
    term_select = [{'id': i + 1, 'name': term.strip()} for i, term in enumerate(term_list)]
    return JsonResponse(term_select, safe=False)    

def manage_bulk_result_new(request):

    course = Course.objects.all()
    examnames = ExamtypeSettings.objects.all()
    sessions = Session.objects.filter(
        is_active=True
    ).first()
    context = {
         'courses': course,
         'examnames': examnames,
        ' page_title': "Manage Bulk Result",
        'sessions': sessions
    }
    return render(request, 'hod_template/manage_bulk_result.html', context)

def delete_bulkresult(request,result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    
    # Clear only the marks (fields might differ based on your model)
    result.test = 0
    result.exam = 0
    result.semester = 0
    result.remarks = ""
    result.save()

    messages.success(request, "Marks cleared successfully.")
    # return redirect('manage_bulk_result_new')
 
    return redirect('manage_bulk_result_new')

def edit_bulkresult(request, result_id):
    instance = get_object_or_404(StudentResult, id=result_id)
    session = Session.objects.filter(is_active=True).first()
    # Get max_marks from ExamtypeSettings
    exam_setting = ExamtypeSettings.objects.filter(
        exam_name=instance.exam_type.exam_name,
        # exam_type=instance.exam_type,
        term=instance.term
    ).first()
    
    max_marks = exam_setting.max_marks if exam_setting else 20

    context = {
        'page_title': 'Edit BulkResult',
        'result': instance,
        'sessions': session,
        'max_marks': max_marks,
        'courses': Course.objects.all(),
        'subjects': Subject.objects.all(),
        'examnames': ExamtypeSettings.objects.all()
    }
    return render(request, 'hod_template/edit_bulk_result.html', context)


def update_student_result_new(request, result_id):
    
    result = get_object_or_404(StudentResult, pk=result_id)

    if request.method == "POST":
        try:
            # Fetch input data
            course_id = request.POST.get('course')
            subject_id = request.POST.get('subject_data_value')
            exam_type_id = request.POST.get('exam_name')
            term = request.POST.get('term_select')
            remarks = request.POST.get('remarks')
            test = request.POST.get('score')
            
            # Get score based on exam type
            exam_type = ExamtypeSettings.objects.get(id=exam_type_id)
            exam_name = exam_type.exam_name.lower()

            if  exam_name:
                test = request.POST.get('score')
        
            else:
                messages.error(request, "Invalid exam type")
                return redirect(request.path)

            # Update result object
            result.student.course_id = course_id
            result.subject_id = subject_id
            result.exam_type_id = exam_type_id
            result.term = term
            result.test = test
            result.remarks = remarks

            result.save()
            messages.success(request, "Result updated successfully")
            return redirect('manage_bulk_result_new')  # Change this to your actual result listing page

        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Error updating result: {str(e)}")

    # Page load (GET request)
    context = {
        "page_title": "Update Student Result",
        "result": result,
        "courses": Student.objects.values('course').distinct(),
        "subjects": Subject.objects.all(),
        "examnames": ExamtypeSettings.objects.all(),
    }
    return render(request, "hod_template/edit_bulk_result.html", context)

def admin_bulk_student_data(request):
    course = request.POST.get('course')
    subject_data1 = request.POST.get('subject')
    term_wise = request.POST.get('term')
    exam_type = request.POST.get('exam')
    try:
        course_obj = get_object_or_404(Course, id=course)
        subject_obj = get_object_or_404(Subject, id=subject_data1)
        examtype_obj = get_object_or_404(ExamtypeSettings, id=exam_type)

        results=StudentResult.objects.filter(
    subject_id=subject_obj.id,
    term=term_wise,
    exam_type_id=examtype_obj.id,
    student__course_id=course_obj.id
)
        bulk_data_list = []
        for r in results:
                data = {
                "student_id": r.id,
                "student_name": f"{r.student.admin.first_name} {r.student.admin.last_name}",
                "admission_number": r.student.admission_number,
                "subject_id": r.subject.id,
                "term": r.term,
                "exam_type_id": r.exam_type.id,
                "exam_type_name": r.exam_type.exam_name.lower(),  # ADD THIS LINE
                "test": r.test,
                "remarks": r.remarks,
                "session_id": r.session.id

}
                bulk_data_list.append(data)

        return JsonResponse(bulk_data_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def get_exam_type_colors_new(request):
    exam_types = ExamtypeSettings.objects.values('exam_type', 'exam_name').distinct()
    
    data = {}
    for item in exam_types:
        data[item['exam_type'].lower()] = item['exam_name']  # You can also include colors here if stored
    return JsonResponse(data)

def admin_studentexamgraph(request):
   courses = Course.objects.all()
   exams= ExamtypeSettings.objects.all()
   sessions = Session.objects.filter(is_active=True).first()
   context = {
       "page_title": "Student Exam Wise Graph",
       "exams": exams,
       "courses": courses,
         "sessions": sessions
   }
   return render(request, "hod_template/admin_studentexamgraph.html", context)
def get_student_bargraph(request):
    student_id = request.GET.get('student_id')
    exam_id = request.GET.get('exam_id')  # exam_type_id
    session_id= request.GET.get('session_id')
    max_mark = ExamtypeSettings.objects.filter(id=exam_id).values_list('max_marks', flat=True).first()
    results = StudentResult.objects.filter(
        student_id=student_id,
        exam_type_id=exam_id,
        session_id=session_id
    ).select_related('subject', 'exam_type')

    subject_marks = []

    for result in results:
        subject_name = result.subject.subject.name
        exam_type = result.exam_type.exam_name.upper()

        # Try fetching value from all possible mark fields
        raw = (
            result.test if result.test not in [None, ''] else
            result.exam if result.exam not in [None, ''] else
            result.semester if result.semester not in [None, ''] else
            None
        )

        # Convert to float safely
        marks = None
        if raw not in [None, '']:
            try:
                marks = float(raw)
            except ValueError:
                marks = None

        subject_marks.append({
            "subject": subject_name,
            "marks": marks
        })

    return JsonResponse({'data': subject_marks,'max_mark': max_mark
    })


def get_max_mark(request):
    exam_id = request.GET.get('exam_id')
    try:
        exam = ExamtypeSettings.objects.get(id=exam_id)
        return JsonResponse({'max_marks': exam.max_marks})
    except ExamtypeSettings.DoesNotExist:
        return JsonResponse({'error': 'Invalid Exam ID'}, status=400)
    
def search(request):  
      course=Course.objects.all()
      school=School.objects.all()
      city = CustomUser.objects.values_list('city', flat=True).distinct()
      district = CustomUser.objects.values_list('district_name', flat=True).distinct()
      context = {
          "page_title": "Search",
            "course": course,
            "cities": city,
            "districts": district,
            "schools":school,
      }
      return render(request, "hod_template/search.html", context)  
@csrf_exempt
def student_search_list(request):
    if request.method == 'GET':
        course = request.GET.get('course', '').strip()
        name = request.GET.get('name', '').strip()
        city = request.GET.get('city', '').strip()
        district = request.GET.get('district', '').strip()
        gender = request.GET.get('gender', '').strip()
        
       

        try:
            filters = Q()

            # --- Filter by Course (supports numeric ID first, fallback to legacy name-division parsing) ---
            if course:
                course_obj = None
                if course.isdigit():
                    course_obj = get_object_or_404(Course, id=course)
                else:
                    # Legacy support: parse string like "10-A" or "QUALIFIERS-H.S. (HIGHER SECONDARY)"
                    if '-' in course:
                        course_name, division = course.rsplit('-', 1)
                    else:
                        course_name, division = course, ''
                    course_obj = Course.objects.filter(
                        name__iexact=course_name.strip(),
                        division__iexact=division.strip()
                    ).first()

                if not course_obj:
                    return JsonResponse({"error": f"No course found for '{course}'"}, status=404)
                filters &= Q(course=course_obj)

            # --- Filter by Name (in CustomUser) ---
            if name:
                filters &= (Q(admin__first_name__icontains=name) | Q(admin__last_name__icontains=name))

            # --- Filter by City (in CustomUser) ---
            if city:
                filters &= Q(admin__city__icontains=city)

            # --- Filter by District (in CustomUser) ---
            if district:
                filters &= Q(admin__district_name__icontains=district)

            # --- Filter by Gender (in CustomUser) ---
            if gender:
                filters &= Q(admin__gender__icontains=gender)

            # --- Execute Query ---
            students = Student.objects.select_related('admin', 'course').filter(filters).values(
                'id',
                'admin__first_name', 'admin__last_name', 'admin__email',
                'admin__city', 'admin__district_name', 'admin__gender',
                'course__name','course__division','guardian_contact_number'
            )
        

            # --- Build JSON Response ---
            results = []
            for s in students:
                results.append({
                    "id": s["id"],
                    "name": f"{s['admin__first_name']} {s['admin__last_name']}",
                    "email": s["admin__email"],
                    "course": f"{s['course__name']} - {s['course__division']}",  # <- include division
                    "city": s["admin__city"],
                    "district": s["admin__district_name"],
                    "gender": s["admin__gender"],
                    "guardian_contact_number": s["guardian_contact_number"],
                })
            return JsonResponse(results, safe=False)

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def add_alumni_admin(request):
    alumniadmin_form = AlumniAdminForm(request.POST or None, request.FILES or None)
    context = {'form': alumniadmin_form, 'page_title': 'Add Alumni Admin'}

    if request.method == 'POST':
        if alumniadmin_form.is_valid():
            try:
                data = alumniadmin_form.cleaned_data

                # Handle profile picture upload
                passport_url = None
                otp_password = str(random.randint(100000, 999999))

                user = CustomUser.objects.filter(email=data['email']).first()
                if user is None:
                    user = CustomUser.objects.create_user(
                        email=data['email'],
                        password=otp_password,
                        user_type='7',
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        profile_pic=None,
                        date_of_birth=data['date_of_birth'],
                        gender=data['gender'],
                        city=data['city'],
                        district_name=data['district_name'],
                        street_address=data['street_address'],
                        state=data['state'],
                        country=data['country'],
                    )
                else:
                    user.user_type = '7'
                    user.otp = otp_password
                    user.set_password(otp_password)
                    user.save()
                user.otp = otp_password
                user.save()

                if 'profile_pic' in request.FILES:
                    save_user_profile_pic(request.FILES['profile_pic'], user)

                AlumniAdmin.objects.update_or_create(
                    alumniadmin=user,
                    defaults={'year_of_passing': data.get('year_of_passing')},
                )

                subject = "Your Alumni Admin Login Details"
                message = f"""
Dear {user.first_name} {user.last_name},

Your Alumni Admin account has been successfully created.

Here are your login credentials:

Email: {user.email}
Password: {otp_password}

Please log in to the portal and change your password for security.

Thank you,
Alumni Management Team
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
                    logger.exception('Error sending email')
                    messages.warning(request, "Alumni Admin added but email failed to send.")

                messages.success(request, "Alumni Admin added and login credentials sent via email.")
                return redirect(reverse('add_alumni_admin'))

            except Exception as e:
                traceback.print_exc()
                messages.error(request, f"Could not add Alumni Admin: {str(e)}")
        else:
            messages.error(request, "Please fulfill all the requirements.")

    return render(request, 'hod_template/add_alumni_admin_template.html', context)    

def manage_alumni_admin(request):
    alumni_Admin = CustomUser.objects.filter(user_type ='7')
    context = {
        'alumni_Admin': alumni_Admin,
       'page_title': 'Manage Alumni Admin'
     }
    return render(request, "hod_template/manage_alumni_admin.html", context)

def edit_alumniAdmin(request, allAdmin):
    alumniadmin_user = get_object_or_404(CustomUser, id=allAdmin, user_type=7)

    if request.method == 'POST':
        form = AlumniAdminForm(request.POST, request.FILES, instance=alumniadmin_user)
        if form.is_valid():
            admin = form.save(commit=False)

            # basic fields update
            admin.first_name = form.cleaned_data.get('first_name')
            admin.last_name = form.cleaned_data.get('last_name')
            admin.city = form.cleaned_data.get('city')
            admin.district_name = form.cleaned_data.get('district_name')
            admin.street_address = form.cleaned_data.get('street_address')
            admin.state = form.cleaned_data.get('state')
            admin.country = form.cleaned_data.get('country')
            admin.email = form.cleaned_data.get('email')
            admin.gender = form.cleaned_data.get('gender')
            admin.date_of_birth = form.cleaned_data.get('date_of_birth')

            # password update
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                admin.set_password(new_password)

            admin.save()
            if 'profile_pic' in request.FILES:
                save_user_profile_pic(request.FILES['profile_pic'], admin)

            messages.success(request, "Profile updated successfully!")
            return redirect(reverse('edit_alumniAdmin', kwargs={'allAdmin': allAdmin}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AlumniAdminForm(instance=alumniadmin_user)

    context = {
        'form': form,
        'id': allAdmin,
        'page_title': 'Edit Profile',
        'user_type': alumniadmin_user.user_type,
    }
    return render(request, 'hod_template/edit_AlumniAdmin_template.html', context)

def delete_alumni_admin(request,allAdmin_id):
     academic_delete = CustomUser.objects.get(id=allAdmin_id)
     delete_user_profile_pic(academic_delete)
     academic_delete.delete()
     messages.success(request, "Successfully Deleted")
     return redirect(reverse('manage_alumni_admin'))


def add_alumni_events(request):
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
            return redirect(reverse('add_alumni_events'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = AlumniEventsForm()

    context = {
        'form': form,
        'page_title': 'Add Alumni Events'
    }
    return render(request, 'hod_template/add_alumni_events_template.html',context)    
    
def  manage_alumni_events(request):
 event = AlumniEventsInfo.objects.all()
 context = {
        'event': event,
        'page_title': 'Manage  Alumni Events'
    }
 return render(request, 'hod_template/manage_alumni_events.html',context )
 
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

    return render(request, 'hod_template/edit_alumni_events.html',context ) 

def delete_alumnievents(request,event_id):
    event = get_object_or_404(AlumniEventsInfo, id=event_id)
    event.delete()
    messages.success(request, "Alumni Event Information is deleted successfully!")
    return redirect(reverse('manage_alumni_events'))      

def add_careerguidanceprogrammes(request):
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
            return redirect(reverse('add_careerguidanceprogrammes'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = CareerGuidanceForm()

    context = {
        'form': form,
        'page_title': 'Add Career Guidance Programme Details'
    }
    return render(request, 'hod_template/add_career_guidance_programme_template.html',context)
def  manage_careerguidanceprogrammes(request):
 programme = CareerGuidance.objects.all()
 context = {
        'programme': programme,
        'page_title': 'Manage  Career Guidance Programme Details'
    }
 return render(request,'hod_template/manage_career_guidance_programme_template.html',context )

def edit_careerguidance_programme(request,programme_id):
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

    return render(request, 'hod_template/edit_career_guidance_template.html',context )  

def delete_careerguidance_programme(request,programme_id):
    programme = get_object_or_404(CareerGuidance, id=programme_id)
    programme.delete()
    messages.success(request, "Career Guidance Programme details deleted successfully!")
    return redirect(reverse('manage_careerguidanceprogrammes')) 

def academic_alumni_settings(request):
    # print("kkkkkk")

    modulesettings = ModuleSettings.objects.all()
    # print("Modulesettings:", modulesettings)

    context = {
        'modulesettings': modulesettings,  # 👈 pass to template
        # 'page_title': "Academic Alumni Settings",
    }

    return render(request, 'hod_template/home_content.html', context) 


def student_promotion(request):
    """Student Promotion page - allows promoting students to the next class/session."""
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {
        'page_title': 'Student Promotion',
        'courses': courses,
        'sessions': sessions,
    }
    return render(request, 'hod_template/student_promotion.html', context)


def promotion_history(request):
    """View to list all student promotions grouped by Session and Class."""
    sessions = Session.objects.all().order_by('-start_year')
    history = []

    for session in sessions:
        # Get promotions for this session
        session_promotions = StudentPromotion.objects.filter(from_session=session).select_related('from_course', 'to_course', 'student', 'student__admin')
        
        if session_promotions.exists():
            batches = {}
            for promo in session_promotions:
                # Group by From Course -> To Course
                # We use the course ID as part of the key to ensure uniqueness
                batch_key = (promo.from_course.id, promo.to_course.id)
                
                if batch_key not in batches:
                    batches[batch_key] = {
                        'from_course': promo.from_course,
                        'to_course': promo.to_course,
                        'promoted_on': promo.promoted_on,
                        'students': [],
                        'count': 0
                    }
                batches[batch_key]['students'].append(promo)
                batches[batch_key]['count'] += 1
            
            # Convert values to list and sort by from_course name (descending)
            batch_list = list(batches.values())
            batch_list.sort(key=lambda x: x['from_course'].name, reverse=True)
            
            history.append({
                'session': session,
                'batches': batch_list
            })

    context = {
        'page_title': 'Promotion History',
        'history': history
    }
    return render(request, 'hod_template/promotion_history.html', context)


@csrf_exempt
def get_promotion_students(request):
    """AJAX: Fetch students by course and optionally session for promotion."""
    from_course = request.POST.get('from_course')
    from_session = request.POST.get('from_session')
    try:
        students = Student.objects.filter(course_id=from_course)
        if from_session:
            students = students.filter(session_id=from_session)

        student_data = []
        for student in students:
            try:
                data = {
                    "id": student.id,
                    "name": student.admin.first_name + " " + student.admin.last_name,
                    "admission_number": student.admission_number if student.admission_number else "N/A",
                    "course": str(student.course) if student.course else "N/A",
                    "session": str(student.session) if student.session else "N/A",
                }
                student_data.append(data)
            except Exception:
                pass 
                
        return HttpResponse(json.dumps(student_data), content_type='application/json')
    except Exception:
        return HttpResponse(json.dumps([]), content_type='application/json')


@csrf_exempt
def promote_students(request):
    """AJAX: Promote selected students to a new course and/or session."""
    try:
        student_ids = json.loads(request.POST.get('student_ids', '[]'))
        to_course = request.POST.get('to_course')
        to_session = request.POST.get('to_session')
        remarks = request.POST.get('remarks', '')

        if not student_ids or not to_course:
            return HttpResponse(json.dumps({
                'status': 'error',
                'message': 'Missing required fields.'
            }), content_type='application/json')

        to_course_obj = Course.objects.get(id=to_course)
        to_session_obj = None
        if to_session:
            to_session_obj = Session.objects.get(id=to_session)

        promoted_count = 0
        
        try:
            with transaction.atomic():
                for student_id in student_ids:
                    try:
                        student = Student.objects.select_for_update().get(id=student_id)
                        
                        # Issue 3 Fix: Check for duplicate promotion
                        if StudentPromotion.objects.filter(
                            student=student,
                            to_course=to_course_obj,
                            to_session=to_session_obj
                        ).exists():
                            continue  # Already promoted, skip
                        
                        # Save promotion history
                        StudentPromotion.objects.create(
                            student=student,
                            from_course=student.course,
                            from_session=student.session,
                            to_course=to_course_obj,
                            to_session=to_session_obj,
                            remarks=remarks
                        )
                        # Update student
                        student.course = to_course_obj
                        if to_session_obj:
                            student.session = to_session_obj
                        student.save()
                        promoted_count += 1
                    except Student.DoesNotExist:
                        continue
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'message': f'Transaction failed: {str(e)}'
            }), content_type='application/json')

        return HttpResponse(json.dumps({
            'status': 'success',
            'message': f'{promoted_count} student(s) promoted successfully!'
        }), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'message': str(e)
        }), content_type='application/json')


def promotion_detail(request, pk):
    """View to show old data of a promoted student."""
    promotion = get_object_or_404(StudentPromotion, pk=pk)
    student = promotion.student
    old_course = promotion.from_course
    old_session = promotion.from_session

    # Fetch old results (subjects in the old course)
    results = StudentResult.objects.filter(
        student=student,
        subject__course=old_course
    )

    # Fetch old attendance (sessions matching old session, subjects in old course)
    attendance_reports = AttendanceReport.objects.filter(
        student=student,
        attendance__session=old_session,
        attendance__subject__course=old_course
    )

    context = {
        'page_title': 'Promotion Detail',
        'promotion': promotion,
        'student': student,
        'results': results,
        'attendance_reports': attendance_reports,
    }
    return render(request, 'hod_template/promotion_detail.html', context)


def undo_promotion(request, promotion_id):
    """Reverts a student promotion."""
    try:
        with transaction.atomic():
            promotion = StudentPromotion.objects.select_for_update().get(id=promotion_id)
            student = Student.objects.select_for_update().get(id=promotion.student_id)
            
            # Revert student state to previous session/course
            student.course = promotion.from_course
            student.session = promotion.from_session
            student.save()
            
            # Delete the promotion record
            promotion.delete()
        
        messages.success(request, "Promotion Reverted Successfully")
    except StudentPromotion.DoesNotExist:
        messages.error(request, "Promotion record not found. It may have already been reverted.")
    except Exception as e:
        messages.error(request, f"Error Reverting Promotion: {e}")
        
    return redirect('promotion_history')




def export_promotion_pdf(request, from_session_id, to_session_id, from_course_id, to_course_id):
    """Exports promotion list to PDF."""
    promotions = StudentPromotion.objects.filter(
        from_session_id=from_session_id,
        to_session_id=to_session_id,
        from_course_id=from_course_id,
        to_course_id=to_course_id
    ).select_related('student', 'student__admin', 'from_course', 'to_course', 'from_session', 'to_session')

    if not promotions.exists():
        messages.error(request, "No promotions found to export.")
        return redirect('promotion_history')

    # Get metadata for template
    first_promo = promotions.first()
    # Issue 4 Fix: Handle NULL sessions safely
    from_session_str = 'N/A'
    to_session_str = 'N/A'
    if first_promo.from_session:
        from_session_str = first_promo.from_session.start_year.strftime('%Y') + "-" + first_promo.from_session.end_year.strftime('%Y')
    if first_promo.to_session:
        to_session_str = first_promo.to_session.start_year.strftime('%Y') + "-" + first_promo.to_session.end_year.strftime('%Y')
    
    context = {
        'promotions': promotions,
        'from_session': from_session_str,
        'to_session': to_session_str,
        'from_course': str(first_promo.from_course),
        'to_course': str(first_promo.to_course),
    }

    # Render HTML
    html_string = render_to_string('pdf_template/promotion_list_pdf.html', context)
    
    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="promotion_list_{from_session_id}_{to_session_id}.pdf"'
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(response)
    
    return response

def manage_parent(request):
    parents = CustomUser.objects.filter(user_type='6')
    context = {
        'parents': parents,
        'page_title': 'Manage Parent Profile'
    }
    return render(request, "hod_template/manage_parent.html", context)

def edit_parent(request, parent_id):
    parent_user = get_object_or_404(CustomUser, id=parent_id)
    parent_obj = get_object_or_404(Parent, admin=parent_user)
    
    initial_data = {
        'joining_date': parent_obj.joining_date,
        'siblings': parent_obj.siblings,
    }
    if parent_obj.students.exists():
        initial_data['students'] = parent_obj.students.all()
        
    form = ParentForm(request.POST or None, request.FILES or None, instance=parent_obj, initial=initial_data)
    
    context = {
        'form': form,
        'parent_id': parent_id,
        'page_title': 'Edit Parent Profile'
    }
    
    if request.method == 'POST':
        student_ids_str = request.POST.get('students', '')
        if student_ids_str:
            student_ids = [int(sid.strip()) for sid in student_ids_str.split(',') if sid.strip().isdigit()]
            post_data = request.POST.copy()
            post_data.setlist('students', student_ids)
            form = ParentForm(post_data, request.FILES or None, instance=parent_obj)
            
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                gender = form.cleaned_data.get('gender')
                street_address = form.cleaned_data.get('street_address')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                district_name = form.cleaned_data.get('district_name')
                country = form.cleaned_data.get('country')
                profile_pic = request.FILES.get('profile_pic')
                date_of_birth = form.cleaned_data.get('date_of_birth')
                
                course = form.cleaned_data.get('course')
                students = form.cleaned_data.get('students')
                joining_date = form.cleaned_data.get('joining_date')
                siblings = form.cleaned_data.get('siblings')
                
                user = parent_obj.admin
                user.email = email
                if password:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.street_address = street_address
                user.city = city
                user.state = state
                user.district_name = district_name
                user.country = country
                user.date_of_birth = date_of_birth
                
                if joining_date:
                    parent_obj.joining_date = joining_date
                if siblings is not None:
                    parent_obj.siblings = siblings
                
                if students is not None:
                    prev_ids = set(parent_obj.students.values_list('id', flat=True))
                    new_ids = set([s.id for s in students])
                    parent_obj.students.set(students)
                    removed_ids = list(prev_ids - new_ids)
                    if removed_ids:
                        Student.objects.filter(id__in=removed_ids).update(parents=None)
                    Student.objects.filter(id__in=list(new_ids)).update(parents=parent_obj)
                
                user.save()
                parent_obj.save()
                if profile_pic:
                    save_user_profile_pic(profile_pic, user)

                messages.success(request, "Parent profile updated successfully!")
                return redirect(reverse('edit_parent', args=[parent_id]))
            except Exception as e:
                messages.error(request, f"Could not update parent: {str(e)}")
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")

    return render(request, 'hod_template/edit_parent.html', context)


def delete_parent(request, parent_id):
    try:
        parent_user = get_object_or_404(CustomUser, id=parent_id)
        delete_user_profile_pic(parent_user)
        parent_user.delete()
        messages.success(request, "Parent profile deleted successfully!")
    except Exception as e:
        messages.error(request, f"Could not delete parent: {str(e)}")
    return redirect(reverse('manage_parent'))
def add_parent(request):
    parent_form = ParentForm(request.POST or None, request.FILES or None)
    context = {'form': parent_form, 'page_title': 'Add Parent Profile'}
    if request.method == 'POST':
        # Handle the comma-separated student IDs from the hidden input
        student_ids_str = request.POST.get('students', '')
        if student_ids_str:
            student_ids = [int(sid.strip()) for sid in student_ids_str.split(',') if sid.strip().isdigit()]
            # Create a new QueryDict with the processed student IDs
            post_data = request.POST.copy()
            post_data.setlist('students', student_ids)
            parent_form = ParentForm(post_data, request.FILES or None)
        
        if parent_form.is_valid():
            try:
                # Extract CustomUser fields
                email = parent_form.cleaned_data.get('email')
                password = parent_form.cleaned_data.get('password')
                first_name = parent_form.cleaned_data.get('first_name')
                last_name = parent_form.cleaned_data.get('last_name')
                gender = parent_form.cleaned_data.get('gender')
                street_address = parent_form.cleaned_data.get('street_address')
                city = parent_form.cleaned_data.get('city')
                state = parent_form.cleaned_data.get('state')
                district_name = parent_form.cleaned_data.get('district_name')
                country = parent_form.cleaned_data.get('country')
                profile_pic = parent_form.cleaned_data.get('profile_pic')
                date_of_birth = parent_form.cleaned_data.get('date_of_birth')
                
                # Extract Parent-specific fields
                course = parent_form.cleaned_data.get('course')
                students = parent_form.cleaned_data.get('students')
                joining_date = parent_form.cleaned_data.get('joining_date')
                siblings = parent_form.cleaned_data.get('siblings')
                
                # Check email uniqueness before creating user
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "The given email is already registered.")
                    return render(request, 'hod_template/add_parent.html', context)

                # Create CustomUser with user_type=5 (Parent)
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    user_type='6',
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    street_address=street_address,
                    city=city,
                    state=state,
                    district_name=district_name,
                    country=country,
                    profile_pic=None,
                    date_of_birth=date_of_birth
                )
                
                # Ensure Parent instance exists (signal may create it); be robust
                parent_obj, _ = Parent.objects.get_or_create(admin=user)
                if joining_date:
                    parent_obj.joining_date = joining_date
                if siblings is not None:
                    parent_obj.siblings = siblings
                
                # Link students to parent (ManyToMany) and sync Student.parents FK
                if students:
                    # capture previously linked student ids (if any)
                    prev_ids = set(parent_obj.students.values_list('id', flat=True))
                    # new selection ids
                    new_ids = set([s.id for s in students])

                    # update the ManyToMany relation
                    parent_obj.students.set(students)

                    # clear parents FK for students removed from this parent
                    removed_ids = list(prev_ids - new_ids)
                    if removed_ids:
                        Student.objects.filter(id__in=removed_ids).update(parents=None)

                    # set parents FK for newly added/selected students
                    Student.objects.filter(id__in=list(new_ids)).update(parents=parent_obj)
                
                parent_obj.save()
                if profile_pic:
                    save_user_profile_pic(profile_pic, user)
                
                messages.success(request, "Parent profile added successfully!")
                return redirect(reverse('add_parent'))
                
            except Exception as e:
                messages.error(request, f"Could not add parent: {str(e)}")
                return render(request, 'hod_template/add_parent.html', context)
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")
            return render(request, 'hod_template/add_parent.html', context)

    return render(request, 'hod_template/add_parent.html', context)
# ------------------- AJAX ENDPOINTS ------------------- #

@csrf_exempt
def get_students_by_course(request):
    """Fetch students filtered by course."""
    course_id = request.GET.get('course_id')
    
    if not course_id:
        return JsonResponse({'error': 'course_id is required'}, status=400)
    
    try:
        students = Student.objects.filter(course_id=course_id).select_related('admin')
       
        student_list = [
            {
                'id': s.id, 
                'name': f"{s.admin.first_name} {s.admin.last_name}",
                'admission_number': s.admission_number
            }
           
            for s in students
        ]
        
        return JsonResponse({'students': student_list})
    except Exception as e:
        logger.error(f"Error fetching students by course: {e}")
        return JsonResponse({'error': 'Error fetching students'}, status=500)

def admin_notify_parent(request):
    """
    Admin page to view parent registration notifications.
    Displays all notifications from ParentAdminNotification table.
    """
    # try:
    # notifications = ParentAdminNotification.objects.select_related('parent__admin').order_by('-created_at')
    notifications = ParentAdminNotification.objects.select_related( 'parent__admin', 'student__admin').order_by('-created_at')    
        # Format datetime objects for template
    notifications_list = []
    for notification in notifications:
            notifications_list.append({
                'id': notification.id,
                 'notifications_list': notifications,
                'parent_name': f"{notification.parent.admin.first_name} {notification.parent.admin.last_name}",
                'parent_email': notification.parent.admin.email,
                'message': notification.message,
                'student_name':f'{notification.student.admin.first_name} {notification.student.admin.last_name}',
                'created_at': notification.created_at.strftime('%d-%m-%Y %H:%M') if notification.created_at else 'N/A',
                'updated_at': notification.updated_at.strftime('%d-%m-%Y %H:%M') if notification.updated_at else 'N/A',
                'status': notification.status,
            })
        
    context = {
            'page_title': "Parent Notifications",
            'notifications_list': notifications_list,
        }
    return render(request, 'hod_template/admin_notify_parent.html', context)

def issue_transfer_certificate(request):
    """
    Display Issue Transfer Certificate page.
    """

    courses = Course.objects.all().order_by("name")
    sessions = Session.objects.all().order_by("-start_year")

    context = {
        "page_title": "Issue Transfer Certificate",
        "courses": courses,
        "sessions": sessions,
    }

    return render(
        request,
        "hod_template/issue_transfer_certificate.html",
        context,
    )

@csrf_exempt
def get_tc_students(request):
    """
    AJAX : Load students for selected class/session.
    """

    try:

        course = request.POST.get("course")
        session = request.POST.get("session")

        students = Student.objects.filter(
            course_id=course,
            status="ACTIVE"
        ).select_related(
            "admin",
            "course",
            "session"
        )

        if session:
            students = students.filter(session_id=session)

        data = []

        for student in students:

            tc_exists = TransferCertificate.objects.filter(
                student=student,
                cancelled=False
            ).exists()

            data.append({
                "id": student.id,
                "admission_number": student.admission_number,
                "name": f"{student.admin.first_name} {student.admin.last_name}",
                "course": str(student.course),
                "session": str(student.session),
                "tc_issued": tc_exists,
            })

        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    except Exception as e:

        return HttpResponse(
            json.dumps([]),
            content_type="application/json"
        )
    
@csrf_exempt
def issue_tc(request):
    """
    Issue Transfer Certificate for selected students.
    """

    try:

        student_ids = json.loads(
            request.POST.get("student_ids", "[]")
            )

        leaving_date = request.POST.get("leaving_date")

        last_attended = request.POST.get("last_attended_date")

        conduct = request.POST.get("conduct")

        qualified = request.POST.get(
            "qualified_for_promotion"
        )

        reason = request.POST.get("reason")

        remarks = request.POST.get("remarks")

        if len(student_ids) == 0:

            return HttpResponse(
                json.dumps({
                    "status": "error",
                    "message": "Please select at least one student."
                }),
                content_type="application/json"
            )

        created = 0
        skipped = 0

        with transaction.atomic():

            for student_id in student_ids:

                try:

                    student = Student.objects.select_for_update().get(
                        id=student_id
                    )

                    existing = TransferCertificate.objects.filter(
                        student=student,
                        cancelled=False
                    ).exists()

                    if existing:
                        skipped += 1
                        continue

                    TransferCertificate.objects.create(

                        student=student,

                        leaving_date=leaving_date,

                        last_attended_date=last_attended
                        if last_attended else None,

                        conduct=conduct,

                        qualified_for_promotion=(
                            True
                            if qualified == "true"
                            else False
                        ),

                        reason=reason,

                        remarks=remarks,

                        issued_by=request.user
                    )

                    student.status = "TRANSFERRED"
                    student.save()

                    created += 1

                except Student.DoesNotExist:
                    continue

        return HttpResponse(
            json.dumps({

                "status": "success",

                "message":
                    f"{created} TC(s) issued successfully. "
                    f"{skipped} skipped."

            }),
            content_type="application/json"
        )

    except Exception as e:

        return HttpResponse(
            json.dumps({

                "status": "error",

                "message": str(e)

            }),
            content_type="application/json"
        )
    
def transfer_certificate_list(request):

    tcs = TransferCertificate.objects.select_related(
    "student",
    "student__admin",
    "student__course",
    "issued_by"
    ).order_by("-created_at")

    context = {
        "page_title": "Transfer Certificate Register",
        "tcs": tcs,
    }

    return render(
        request,
        "hod_template/transfer_certificate_list.html",
        context
    )


def transfer_certificate_detail(request, tc_id):

    tc = TransferCertificate.objects.select_related(
        "student",
        "student__admin",
        "student__course",
        "student__session",
        "issued_by",
    ).get(id=tc_id)

    context = {
        "page_title": "Transfer Certificate Details",
        "tc": tc,
    }

    return render(
        request,
        "hod_template/transfer_certificate_detail.html",
        context
    )


@csrf_exempt
def cancel_transfer_certificate(request):

    if request.method != "POST":

        return HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Invalid Request"
            }),
            content_type="application/json"
        )

    try:

        tc_id = request.POST.get("tc_id")

        with transaction.atomic():

            tc = TransferCertificate.objects.select_for_update().get(
                id=tc_id
            )

            if tc.cancelled:

                return HttpResponse(
                    json.dumps({
                        "status": "error",
                        "message": "Transfer Certificate already cancelled."
                    }),
                    content_type="application/json"
                )

            tc.cancelled = True
            tc.save()

            student = tc.student
            student.status = "ACTIVE"
            student.save()

        return HttpResponse(
            json.dumps({
                "status": "success",
                "message": "Transfer Certificate cancelled successfully."
            }),
            content_type="application/json"
        )

    except TransferCertificate.DoesNotExist:

        return HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Transfer Certificate not found."
            }),
            content_type="application/json"
        )

    except Exception as e:

        return HttpResponse(
            json.dumps({
                "status": "error",
                "message": str(e)
            }),
            content_type="application/json"
        )
    


@csrf_exempt
def delete_transfer_certificate(request):

    if request.method != "POST":

        return HttpResponse(
            json.dumps({
                "status": "error"
            }),
            content_type="application/json"
        )

    try:

        tc_id = request.POST.get("tc_id")

        with transaction.atomic():

            tc = TransferCertificate.objects.select_for_update().get(
                id=tc_id
            )

            student = tc.student

            tc.delete()

            student.status = "ACTIVE"
            student.save()

        return HttpResponse(
            json.dumps({
                "status": "success",
                "message": "Transfer Certificate deleted successfully."
            }),
            content_type="application/json"
        )

    except Exception as e:

        return HttpResponse(
            json.dumps({
                "status": "error",
                "message": str(e)
            }),
            content_type="application/json"

        )

def print_transfer_certificate(request, tc_id):

    tc = TransferCertificate.objects.select_related(
        "student",
        "student__admin",
        "student__course",
        "student__session",
        "issued_by",
    ).get(id=tc_id)

    context = {
        "tc": tc,
        "student": tc.student,
    }

    html_string = render_to_string(
        "pdf_template/transfer_certificate.html",
        context
    )

    html = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    )

    pdf = html.write_pdf()

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="{tc.tc_number}.pdf"'
    )

    return response


@csrf_exempt
def print_selected_transfer_certificates(request):

    ids = request.POST.getlist("tc_ids")

    tcs = TransferCertificate.objects.filter(
        id__in=ids
    ).select_related(
        "student",
        "student__admin",
        "student__course",
        "student__session",
        "issued_by",
    )

    context = {

        "tcs": tcs

    }

    html_string = render_to_string(

        "pdf_template/bulk_transfer_certificate.html",

        context

    )

    html = HTML(

        string=html_string,

        base_url=request.build_absolute_uri("/")

    )

    pdf = html.write_pdf()

    response = HttpResponse(

        pdf,

        content_type="application/pdf"

    )

    response["Content-Disposition"] = (

        'inline; filename="TransferCertificates.pdf"'

    )

    return response

def reprint_transfer_certificate(request, tc_id):

    return print_transfer_certificate(
        request,
        tc_id
    )


def print_transfer_certificate_register(request):

    tcs = TransferCertificate.objects.select_related(
        "student",
        "student__admin",
        "student__course",
    ).order_by("-created_at")

    context = {

        "tcs": tcs

    }

    html_string = render_to_string(

        "pdf_template/transfer_certificate_register.html",

        context

    )

    html = HTML(

        string=html_string,

        base_url=request.build_absolute_uri("/")

    )

    pdf = html.write_pdf()

    response = HttpResponse(

        pdf,

        content_type="application/pdf"

    )

    response["Content-Disposition"] = (

        'inline; filename="TC_Register.pdf"'

    )

    return response


@csrf_exempt
def duplicate_transfer_certificate(request, tc_id):

    tc = TransferCertificate.objects.get(
        id=tc_id
    )

    context = {

        "tc": tc,

        "duplicate": True

    }

    html_string = render_to_string(

        "pdf_template/transfer_certificate.html",

        context

    )

    pdf = HTML(

        string=html_string,

        base_url=request.build_absolute_uri("/")

    ).write_pdf()

    return HttpResponse(

        pdf,

        content_type="application/pdf"

    )
# def approve_notification(request, id):

#     notification = get_object_or_404(ParentAdminNotification, id=id)

#     if notification.status == "Pending":

#         student = notification.student
#         parent = notification.parent

#         # ✅ Update student parents_id
#         student.parents_id = parent.id
#         student.save()

#         # ✅ Update notification status
#         notification.status = "Approved"
#         notification.verified_at = timezone.now()
#         notification.save()

#         messages.success(request, "Student linked to parent and approved successfully.")

#     else:
#         messages.warning(request, "Already processed.")

#     return redirect('admin_notify_parent')
   
# def approve_notification(request, id):

#     notification = get_object_or_404(ParentAdminNotification, id=id)

#     if notification.status == "Pending":

#         student = notification.student
#         parent = notification.parent

#         # ✅ Update student parents_id
#         student.parents_id = parent.id
#         student.save()

#         # ✅ Insert into parent_students table (avoid duplicates)
#         Student.objects.get_or_create(
#              parents_id=student.parents_id
#             # student_id=student.id
#         )

#         # ✅ Update notification status
#         notification.status = "Approved"
#         notification.verified_at = timezone.now()
#         notification.save()

#         messages.success(request, "Student linked to parent and approved successfully.")

#     else:
#         messages.warning(request, "Already processed.")

#     return redirect('admin_notify_parent')

def approve_notification(request, id):

    notification = get_object_or_404(ParentAdminNotification, id=id)

    if notification.status == "Pending":

        student = notification.student
        parent = notification.parent

        # ✅ Just update ForeignKey
        student.parents = parent
        student.save()

        notification.status = "Approved"
        notification.verified_at = timezone.now()
        notification.save()

        messages.success(request, "Student linked to parent successfully.")

    else:
        messages.warning(request, "Already processed.")

    return redirect('admin_notify_parent')
