import json

from django.db import IntegrityError
from main_app.models import Subject, Course, Subjectmaster
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django import forms
import random
from django.core.mail import send_mail
from django.conf import settings
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
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
from .models import Student
from .models import CustomUser
# from .forms import AlumnimembersForm
# from .models import Alumnimembers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash

import openpyxl

from .forms import ExcelUploadForm
from django.shortcuts import render
import pandas as pd
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from io import BytesIO
from openpyxl.utils.dataframe import dataframe_to_rows  # Correct import
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
import smtplib
from email.mime.text import MIMEText
def alumnis_home(request):
    total_jobpostings = CareerInfo.objects.count()
    total_events = AlumniEventsInfo.objects.count()
    total_guidance = CareerGuidance.objects.count()
    total_alumni = Alumnimembers.objects.filter(is_active=True).count()
    
    alumni_profile = Alumnimembers.objects.filter(admin=request.user).first()
    
    recent_events = AlumniEventsInfo.objects.all().order_by('-id')[:5]
    recent_jobs = CareerInfo.objects.all().order_by('-id')[:5]

    # Filter group memberships safely
    joined_groups = []
    try:
        memberships = GroupMembership.objects.filter(user=request.user)
        for membership in memberships.filter(notified=False):
            membership.notified = True
            membership.save()
        joined_groups = [m.chat_group for m in memberships]
    except Exception:
        pass

    context = {
        'page_title': "Alumni Dashboard",
        'total_jobpostings': total_jobpostings,
        'total_events': total_events,
        'total_guidance': total_guidance,
        'total_alumni': total_alumni,
        'alumni_profile': alumni_profile,
        'recent_events': recent_events,
        'recent_jobs': recent_jobs,
        'joined_groups': joined_groups,
    }
    return render(request, 'alumni_template/home_content.html', context)

# @login_required(login_url='login_page')
# def alumni_student_view_profile(request):
#     """
#     Alumni profile view/edit page.
#     """
#     from .forms import AlumniProfileEditForm
#     from django.core.files.storage import FileSystemStorage

#     user = request.user
#     form = AlumniMembersForm(request.POST or None, request.FILES or None, instance=user)
#     context = {
#         'form': form,
#         'page_title': 'View/Edit Profile'
#     }

#     if request.method == 'POST':
#         try:
#             if form.is_valid():
#                 password = form.cleaned_data.get('password') or None
#                 passport = request.FILES.get('profile_pic') or None

#                 if password:
#                     user.set_password(password)
#                 if passport:
#                     fs = FileSystemStorage()
#                     filename = fs.save(passport.name, passport)
#                     passport_url = fs.url(filename)
#                     user.profile_pic = passport_url

#                 form.save()
#                 messages.success(request, "Profile Updated!")
#                 return redirect(reverse('alumni_student_view_profile'))
#             else:
#                 messages.error(request, "Invalid Data Provided")
#         except Exception as e:
#             messages.error(request, "Error Occurred While Updating Profile: " + str(e))

#     return render(request, "alumni_template/alumni_student_view_profile.html", context)



def alumni_student_view_profile(request):
    user = request.user

    alumni, created = Alumnimembers.objects.get_or_create(admin=user)

    form = AlumniMembersForm(
        request.POST or None,
        request.FILES or None,
        instance=alumni,
        user=user
    )

    if request.method == 'POST' and form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        form.save()
        passport = request.FILES.get('profile_pic')
        if passport:
            save_user_profile_pic(passport, user)
        messages.success(request, "Profile Updated!")
        return redirect('alumni_student_view_profile')

    return render(request, "alumni_template/alumni_student_view_profile.html", {
        'form': form,
        'page_title': 'View/Edit Profile'
    })
@login_required(login_url='login_page')
def placement_cell(request):
    """
    View to display job notifications (Placement Cell).
    """
    from .models import CareerInfo
    info = CareerInfo.objects.all().order_by('-created_at')
    context = {
        'info': info,
        'page_title': 'Placement Cell (Job Notifications)'
    }
    return render(request, "alumni_template/placement_cell.html", context)
@login_required(login_url='login_page')
def view_events(request):
    """
    View to display upcoming alumni events.
    """
    from .models import AlumniEventsInfo
    info = AlumniEventsInfo.objects.all().order_by('-event_date')
    context = {
        'info': info,
        'page_title': 'Alumni Events'
    }
    return render(request, "alumni_template/view_events.html", context)
@login_required(login_url='login_page')
def view_careerguidance(request):
    """
    View to display career guidance programmes.
    """
    from .models import CareerGuidance
    programme = CareerGuidance.objects.all().order_by('-programme_date')
    context = {
        'programme': programme,
        'page_title': 'Career Guidance Programmes'
    }
    return render(request, "alumni_template/view_careerguidance.html", context)

@login_required(login_url='login_page')
def alumni_feedback(request):
    """
    View to allow Alumni to submit feedback and view past feedback.
    """
    from .forms import AlumniFeedbackForm
    from .models import AlumniFeedback, Alumnimembers
    
    # alumni_profile = Alumnimembers.objects.filter(email=request.user.email).first()
    alumni_profile = Alumnimembers.objects.filter(admin_id=request.user.id).first()
    if not alumni_profile:
        alumni_profile = Alumnimembers.objects.filter(admin_id=request.user).first()
        if not alumni_profile:
            # For testing purposes, if no profile exists, create a dummy one or gracefully deny
            alumni_profile, _ = Alumnimembers.objects.get_or_create(
                email=request.user.email,
                defaults={
                    # 'first_name': request.user.first_name or 'Alumni User',
                    'alumnimembers': request.user,
                    'gender': 'O',  # Other as default
                    'current_status': 'E'
                }
            )

    form = AlumniFeedbackForm(request.POST or None)
    
    context = {
        'form': form,
        'feedbacks': AlumniFeedback.objects.filter(alumni=alumni_profile).order_by('-created_at'),
        'page_title': 'Alumni Feedback'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.alumni = alumni_profile
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('alumni_feedback'))
            except Exception as e:
                messages.error(request, "Could not submit! " + str(e))
        else:
            messages.error(request, "Form has errors!")

    return render(request, "alumni_template/alumni_feedback.html", context)
@login_required(login_url='login_page')
def alumni_list(request):
    """
    Shows other alumni members from the same course and batch.
    """
    from .models import Alumnimembers
    current_user = request.user
    
    # alumni_profile = Alumnimembers.objects.filter(email=request.user.email).first()
    alumni_profile = Alumnimembers.objects.filter(admin_id=request.user.id).first()
   
    if not alumni_profile:
       alumni_profile = Alumnimembers.objects.filter(admin_id=request.user.id).first()
        
    if alumni_profile:
        batch = alumni_profile.period_of_study
        course = alumni_profile.course_studied

        if course and batch:
            # Show others with the same course and batch, excluding the user themselves
            alumni_members = Alumnimembers.objects.filter(
                course_studied=course,
                period_of_study=batch
            ).exclude(id=alumni_profile.id)
        else:
            alumni_members = Alumnimembers.objects.none()

        context = {
            "alumni_members": alumni_members,
            "page_title": "Alumni Members List"
        }
        return render(request, "alumni_template/alumni_chatlist.html", context)

    # If the user hasn't completed their alumni profile yet
    return redirect("alumni_home")


@login_required(login_url='login_page')
def alumni_password(request):
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm
    import smtplib
    from email.mime.text import MIMEText

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This is important to keep the session alive after password change
            update_session_auth_hash(request, user)

            # Send confirmation email (Optional - Configure SMTP settings in your project first)
            try:
                subject = "Your Alumni Account Password Has Been Changed"
                message = f"Dear {user.first_name}, your password has been successfully updated. If you did not make this change, please contact us immediately."
                
                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = 'your-email@gmail.com'
                msg['To'] = user.email

                # Note: Configure your actual SMTP credentials here or in settings.py
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('your-email@gmail.com', 'your-app-password') 
                server.send_message(msg)
                server.quit()
            except Exception as e:
                messages.warning(request, 'Password updated, but email notification failed.')

            messages.success(request, 'Your password was successfully updated!')
            return redirect('alumni_home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'page_title': 'Change Password'
    }
    return render(request, 'alumni_template/alumni_password_template.html', context)
