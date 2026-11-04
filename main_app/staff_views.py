import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse,HttpResponseServerError
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import traceback
from weasyprint import HTML
from weasyprint import HTML, CSS
from .forms import *
from .models import * 
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Concat, Replace, Upper
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from main_app.models import StudentResult
from main_app.forms import EditResultForm , ExamtypeSettings 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import traceback
from collections import defaultdict
from main_app.models import ExamtypeSettings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
import os
from django.template.loader import render_to_string
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
from django.conf import settings
from django.utils import timezone
# from weasyprint import HTML, CSS  # Removed due to missing GTK+ dependencies on Windows
from django.db.models import Value, F
import pathlib

@login_required
def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.filter(course=staff.course).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.filter(staff=staff)
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    course_list = Course.objects.all()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.last_name) + ' (' + str(staff.course) + ')',
        'total_students': total_students,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'course_list': course_list,
        'attendance_list': attendance_list
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_take_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    # subjects = Subject.objects.filter(staff_id=staff)
    # subjects =Subject.objects.filter(staff_id=staff.id).values("subject_id").distinct()
    # print(subjects)
    # subjectmaster = Subjectmaster.objects.get(id=subjects)
    subjects = Subject.objects.filter(staff_id=staff)
       
    sessions = Session.objects.all()
    context = {
         'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Take Attendance',
        # 'subjects': subject_list 
    }
    return render(request, 'staff_template/staff_take_attendance.html', context)


@csrf_exempt
def get_students(request):
    course_id = request.POST.get('course')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    print( subject_id, session_id)
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        course = get_object_or_404(Course, id=course_id)


        students = Student.objects.filter(course_id=course)
        examname = ExamtypeSettings.objects.all()
        student_data = []
        for student in students:
            data = {
                    "id": student.id,
                    "name": student.admin.first_name + " " + student.admin.last_name,
                    # "examname": examname
                    }
            student_data.append(data) 
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def save_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    students = json.loads(student_data)
    try:
        session = get_object_or_404(Session, id=session_id)
        subject = get_object_or_404(Subject, id=subject_id)

        # Check if an attendance object already exists for the given date and session
        attendance, created = Attendance.objects.get_or_create(session=session, subject=subject, date=date)

        for student_dict in students:
            student = get_object_or_404(Student, id=student_dict.get('id'))

            # Check if an attendance report already exists for the student and the attendance object
            attendance_report, report_created = AttendanceReport.objects.get_or_create(student=student, attendance=attendance)

            # Update the status only if the attendance report was newly created
            if report_created:
                attendance_report.status = student_dict.get('status')
                attendance_report.save()

    except Exception as e:
        return None

    return HttpResponse("OK")


def staff_update_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff_id=staff)
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request, 'staff_template/staff_update_attendance.html', context)


@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        student_data = []
        for attendance in attendance_data:
            data = {"id": attendance.student.admin.id,
                    "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
                    "status": attendance.status}
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    students = json.loads(student_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for student_dict in students:
            student = get_object_or_404(
                Student, admin_id=student_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
            attendance_report.status = student_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def staff_apply_leave(request):
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    if request.method == 'POST':
        form = LeaveReportStaffForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                leave_report = form.save(commit=False)
                leave_report.staff = staff
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save(f"leave_images/{image.name}", image)
                    leave_report.image = filename
                leave_report.save()
                messages.success(request, "Application for leave has been submitted for review")
                return redirect(reverse('staff_apply_leave'))
            except Exception as e:
                messages.error(request, f"Could not apply! Error: {str(e)}")
        else:
            messages.error(request, "Form has errors!")
    else:
        form = LeaveReportStaffForm()

    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(staff=staff),
        'page_title': 'Apply for Leave'
    }
    return render(request, "staff_template/staff_apply_leave.html", context)

def edit_staff_leave(request,leave_id):
    leave_report = get_object_or_404(LeaveReportStaff, id=leave_id, staff__admin_id=request.user.id)
    if request.method == 'POST':
        form = LeaveReportStaffForm(request.POST, request.FILES, instance=leave_report)
        if form.is_valid():
            try:
                updated_leave = form.save(commit=False)
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save(f"leave_images/{image.name}", image)
                    updated_leave.image = filename
                updated_leave.save()
                messages.success(request, "Leave application has been updated successfully")
                return redirect(reverse('staff_apply_leave'))
            except Exception as e:
                messages.error(request, f"Could not update! Error: {str(e)}")
        else:
            messages.error(request, "Form has errors!")
    else:
        form = LeaveReportStaffForm(instance=leave_report)
    
    context = {
        'form': form,
        'leave_report': leave_report,
        'page_title': 'Edit Leave Application'
    }
    return render(request, "staff_template/edit_staff_leave_template.html", context)

def delete_staff_leave(request, leave_id):
    leave_report = get_object_or_404(LeaveReportStaff, id=leave_id, staff__admin_id=request.user.id)
    try:
        leave_report.delete()
        messages.success(request, "Leave application has been deleted successfully")
    except Exception as e:
        messages.error(request, f"Could not delete! Error: {str(e)}")
    return redirect(reverse('staff_apply_leave'))


def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('staff_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    admin = staff.admin

    form = StaffEditForm(request.POST or None, request.FILES or None, instance=admin)

    if request.method == 'POST':
        try:
            if form.is_valid():
                passport = request.FILES.get('profile_pic')
                updated_user = form.save(commit=False)
                new_password = form.cleaned_data.get('new_password')

                if new_password:  # Only update password if entered
                    updated_user.set_password(new_password)

                if passport:
                    updated_user.profile_pic = admin.profile_pic

                updated_user.save()
                staff.save()

                if passport:
                    save_user_profile_pic(passport, updated_user)

                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid data provided.")
        except Exception as e:
            messages.error(request, "Error occurred: " + str(e))

    context = {'form': form, 'page_title': 'View/Update Profile'}
    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)

@login_required
def staff_add_result2(request):
    staff = get_object_or_404(Staff, admin=request.user)

    # Fetch subjects and sessions
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject').distinct()
    sessions = Session.objects.all()
    examnames = ExamtypeSettings.objects.all()
    subjects_data=StudentResult.objects.select_related('subject').filter(subject__staff=staff.id)
    # Get all distinct courses taught by this staff through related subjects
    data_list = Course.objects.filter(subject__staff_id=staff.id).distinct()
    # Prepare context
    context = {
        'page_title': 'Result Upload',
        'subjects': subjects,
        'sessions': sessions,
        'examnames': examnames,
         'data_list': data_list,
        #  'data_list': [{'course': subject.course} for subject in subjects],
    }

    # Handle form POST
    if request.method == "POST":
        try:
            student_id = request.POST.get("student_list")
            subject_id = request.POST.get("subject")  # ✅ Corrected name
            exam_name_id = request.POST.get("exam_name")
            term = request.POST.get("term")
            remarks = request.POST.get("remarks")
            course_id = request.POST.get("course1")
            test = request.POST.get("test")
            exam = request.POST.get("exam")
            semester = request.POST.get("semester_score")
            test_score = float(test) if test else 0
            exam_score = float(exam) if exam else 0
            semester_score = float(semester) if semester else 0

            # ✅ Only one of test, exam, semester should be non-zero
            non_zero_fields = sum([
                1 if test_score > 0 else 0,
                1 if exam_score > 0 else 0,
                1 if semester_score > 0 else 0
            ])

            if non_zero_fields != 1:
                return render(request, "staff_template/staff_add_result2.html", {
                    "error": "Only one score type should be entered (Test / Exam / Semester).",
                    **context
                })

            # Get subject record using staff, course, and subject ID
            sub = get_object_or_404(Subject, staff=staff, course_id=course_id, subject_id=subject_id)
            subjectmaster = sub.subject

            # Fetch model instances
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            exam = get_object_or_404(ExamtypeSettings, id=exam_name_id)

            # Update or create student result
            result, created = StudentResult.objects.update_or_create(
                student=student,
                subject=subject,
                exam_type=exam,
                term=term,
                defaults={
                    'subjectmaster': subjectmaster,
                    'test': test_score,
                    'exam': exam_score,
                    'semester': semester_score,
                    'remarks': remarks
                }
            )
            if created:
                message = "Result inserted successfully."
            else:
              message = "Result updated successfully."

            # Save (not strictly necessary with update_or_create, but safe)
            result.save()

            return render(request, "staff_template/staff_add_result2.html", {
                "success": True,
                "message": "Result inserted successfully." if created else "Result updated successfully.",
                **context
            })

        except Exception as e:
            print("Error during result save:")
            print(traceback.format_exc())  # ✅ Debug full traceback in console
            return render(request, "staff_template/staff_add_result2.html", {
                "error": f"Error: {str(e)}",
                **context
            })

    # GET request fallback
    return render(request, "staff_template/staff_add_result2.html", context)

def staff_add_result(request):
    staff = get_object_or_404(Staff, admin=request.user)

    # Fetch subjects and sessions
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject').distinct()
    sessions = Session.objects.all()

    # Prepare context
    context = {
        'page_title': 'Result Upload',
        'subjects': subjects,
        'sessions': sessions,
        'data_list': [{'course': subject.course} for subject in subjects],
    }

    if request.method == 'POST':
        try:
            # Extracting form data
            student_id = request.POST.get('student_list')
            subject_id = request.POST.get('subject')
            course_id = request.POST.get('course1')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            remarks = request.POST.get('remarks')
            term = request.POST.get('term')

            # print("Received data:", student_id, subject_id, course_id, test, exam, remarks, term)

            # Validate required fields
            if not all([student_id, subject_id, course_id, test, exam, term]):
                messages.warning(request, "All fields are required.")
                return render(request, "staff_template/staff_add_result.html", context)

            # Fetch related objects
            student = get_object_or_404(Student, id=student_id)

            # Ensure Subject exists for the staff and matches course/subject
            sub = get_object_or_404(Subject, staff=staff, course_id=course_id, subject_id=subject_id)

            # Fetch corresponding Subjectmaster
            subjectmaster = sub.subject

            # print("Subject ID:", sub.id, "Subjectmaster ID:", subjectmaster.id)

            # Check if result exists, update if it does, create if not
            result, created = StudentResult.objects.update_or_create(
                student=student,
                subject=sub,  # Pass the Subject instance
                subjectmaster=subjectmaster,  # Pass the Subjectmaster instance
                term=term,
                defaults={
                    'test': test,
                    'exam': exam,
                    'remarks': remarks,
                }
            )

            if created:
                messages.success(request, "Scores Saved")
            else:
                messages.success(request, "Scores Updated")

        except Exception as e:
            print("Error Occurred:", e)
            messages.warning(request, f"Error Occurred While Processing Form: {e}")

    return render(request, "staff_template/staff_add_result.html", context)



@csrf_exempt
def fetch_student_result(request):
    try:
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        # Fetch the student and subject using get_object_or_404
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subjectmaster, id=subject_id)
        # Fetch student result
        results = StudentResult.objects.filter(student=student, subject=subject)
        # Prepare JSON data
        json_data = []
        for result in results:
            result_data = {
                'exam': result.exam,
                'test': result.test,
                'remarks': result.remarks,
                'term': result.term
            }
            json_data.append(result_data)

          # Return JSON response
        return JsonResponse(json_data, safe=False)

    except Exception as e:
        # Log the exception or provide more detailed error information
        print(f"Error occurred: {str(e)}")
        return HttpResponseServerError(f"Error occurred: {str(e)}")

# Simulating the execution
print("This is a simulation of the fetch_student_result function.")
print("In a real Django environment, this function would be called when a POST request is made to the corresponding URL.")

def staff_curriculam(request):
    staff = get_object_or_404(Staff, admin=request.user)

    # Get all Subject entries linked to this staff
    subjects = Subject.objects.filter(staff=staff)

    # Filter Curriculam entries linked to these Subject instances
    results = Curriculam.objects.filter(subject__in=subjects).order_by('term')

    data_list = []
    for result in results:
        data = {
            'id': result.id,
            'course': result.course.name,
            'subject': result.subject.subject.name,  # subjectmaster name
            'lesson': result.lesson,
            'term': result.term,
            'status': result.status,
        }
        data_list.append(data)

    return render(request, "staff_template/staff_curriculum.html", {
        'results': data_list,
        'page_title': "Curriculum Assigned to Me",
    })
@csrf_exempt
def tick_status(request):

     # Get selected values from the request
     selected_values = request.POST.getlist('selectedValues[]')  # List of strings

# Clean and validate input values
     cleaned_ids = []
     for val in selected_values:
         try:
           cleaned_ids.append(int(val.strip("'").strip()))  # Remove quotes/whitespace and convert to int
         except ValueError:
          print(f"Skipping invalid value: {val}")  # Log invalid values

# Debugging: Print the cleaned IDs

    #  print("Cleaned IDs to update:", cleaned_ids)

# Proceed with database update only if there are valid IDs
     if cleaned_ids:
       updated_rows = Curriculam.objects.filter(id__in=cleaned_ids).update(status=1)
       print(f"{updated_rows} rows updated.")
     else:
        print("No valid IDs provided.")

     return render(request, "acc_admin_template/staff_curriculum.html",{'curriculam_data'})

def manage_student_result(request):
    # Get the staff object for the logged-in user
    staff = get_object_or_404(Staff, admin=request.user)
    subjects_data=StudentResult.objects.select_related('subject').filter(subject__staff=staff.id)
    # Get all distinct courses taught by this staff through related subjects
    data_list = Course.objects.filter(subject__staff_id=staff.id).distinct()

    context = {
        'page_title': 'Manage Student Result',
        'data_list': data_list,
        'subjects_data': subjects_data,
    }

    return render(request, "staff_template/manageresult_template.html", context)


def manage_student_result_new(request):
    # Get the staff object for the logged-in user
    staff = get_object_or_404(Staff, admin=request.user)
    subjects_data=StudentResult.objects.select_related('subject').filter(subject__staff=staff.id)
    # Get all distinct courses taught by this staff through related subjects
    data_list = Course.objects.filter(subject__staff_id=staff.id).distinct()

    context = {
        'page_title': 'Manage Student Result',
        'data_list': data_list,
        'subjects_data': subjects_data,
    }

    return render(request, "staff_template/manageresultnew_template.html", context)



def edit_result(request, id):
    result = get_object_or_404(StudentResult, id=id)
    examname = ExamtypeSettings.objects.all()
    form = EditResultForm(request.POST, instance=result)
    staff = get_object_or_404(Staff, admin=request.user)
    if request.method == 'POST':
        form = EditResultForm(request.POST, instance=result)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Result updated successfully.")
                return redirect('manage_student_result')
            except Exception as e:
                messages.error(request, f"Error while saving: {e}")
        else:
            print(form.errors)
            messages.error(request, "The form is invalid.")
    else:
        form = EditResultForm(instance=result)

    selected_exam_id = result.exam_type_id

    context = {
        'form': form,
        'examname': examname,
        'selected_exam_id': selected_exam_id,
        'page_title': 'Edit Result'
    }

    return render(request, "staff_template/edit_result_template.html", context)

def delete_result(request, id):
    result = get_object_or_404(StudentResult, id=id)
    try:
        result.delete()
        messages.success(request, "Result Deleted")
    except Exception as e:
        messages.error(request, f"Could not delete! Error: {str(e)}")
    return redirect(reverse('manage_student_result'))
@csrf_exempt
def select_termwise(request):
       if request.method == 'POST':
        # Get the current staff based on the logged-in user
        staff = get_object_or_404(Staff, admin=request.user)

        # Get the term from the request
        term = request.POST.get('term_wise')
        course=request.POST.get('course1')
        subject=request.POST.get('subject')
      
        student_results = StudentResult.objects.filter( student__course_id=course, subject_id=subject, term=term
).select_related('student', 'subject', 'student__course')

    #     subjects = Subject.objects.filter(staff_id=staff.id, course_id=course, subject_id=subject).values('id')
    #     subject_ids = [subject['id'] for subject in subjects]
    #     print("Selected Subject IDs:", subject_ids)
    #    # student_results = StudentResult.objects.filter(subject_id__in=subject_ids).order_by('student__course_id', 'term', 'subject_id')
    #     student_results = StudentResult.objects.filter(subject_id__in=subject_ids, term=term)
    #     print("Student Results:", student_results)
        subject_list = []
        for result in student_results:
         
         subject_list.append({
                "id": result.id,
                "student_name": f"{result.student.admin.first_name} {result.student.admin.last_name}",
                "course": f"{result.student.course.name}-{result.student.course.division}",
                "subject": result.subjectmaster.name,
                "test": result.test,
                "exam_type": result.exam_type.exam_name,
                "remarks": result.remarks,
                "term": result.term,
                "edit_url": f"/staff/edit_result/{result.id}",
                "delete_url": f"/staff/delete_result/{result.id}"
        })
       
        return JsonResponse(subject_list, safe=False)  # No need for json.dumps

       return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt
def staff_get_course(request):
    course_id = request.POST.get('course')
    staff = get_object_or_404(Staff, admin=request.user)
    subject_names = Subject.objects.filter(course_id=course_id, staff_id=staff.id)
    subject_data = []
    for subject_name in subject_names:
        data = {
                 "id": subject_name.subject.id,
                 "name": subject_name.subject.name 
                }
        subject_data.append(data) 
    return JsonResponse(json.dumps(subject_data), content_type='application/json', safe=False)
def lesson_notes(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = LessonSettingsForm(request.POST, request.FILES, instance=staff)
    if not request.user.is_authenticated or not hasattr(request.user, 'staff'):
        return redirect('login')
    subject = Subject.objects.filter(staff=staff).select_related('course', 'subject').distinct()
    subjects = Subject.objects.filter(staff=staff)
    curriculam = request.POST.get('subject_data2')
    subject_list = []
    for subject in subjects:
        subject_list.append({
            'id': subject.id,
            'name': subject.subject.name,
            'course': subject.course.name if subject.course else "",
            'division': subject.course.division if subject.course.division else "",
            'subjects': subject,
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    subject_data = [{'id': subject['id'], 'name': subject['name'], 'course': subject['course'], 'division': subject['division']} for subject in subject_list]
    if request.method == 'POST':
        form = LessonSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            subject = subject.id
            curriculam =request.POST.get('subject_data2')
            date = form.cleaned_data.get('date')
            notes = form.cleaned_data.get('notes')
            image = form.cleaned_data.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                image_url = fs.url(filename)
            else:
                image_url = None

            # Save to the LessonSettings model
            LessonSettings.objects.create(
                subject_id=subject,
                curriculam_id=curriculam,
                date=date,
                notes=notes,
                image=image_url if image_url else None
            )

            messages.success(request, "Lesson notes successfully added.")
            return redirect(reverse('lesson_notes'))
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LessonSettingsForm()

    context = {
        'page_title': 'Lesson Notes',
        'form': form,
        'subject_list': subject_list,
        'subjects': subjects,
    }
    return render(request, "staff_template/staff_lesson_notes_template.html", context)
@csrf_exempt
def staff_get_curriculam(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subject = request.POST.get('subject')
    course = request.POST.get('course')
    curriculams = Curriculam.objects.filter(course_id=(course),subject_id=(subject),subject__staff_id=staff.id).select_related('subject')
  
    
    curriculam_data = []

    for curriculam in curriculams:
        curriculam_data.append({
            "id": curriculam.id,
            "title": curriculam.title,
           
        })
       
    return JsonResponse(json.dumps(curriculam_data), content_type='application/json', safe=False)



def view_filtered_class_results_by_subject(request):
    courses = Course.objects.all()
    selected_course_id = request.GET.get('course')
    selected_subject_id = request.GET.get('subject')

    # Get subjects based on selected course
    subjects = Subject.objects.filter(course__id=selected_course_id) if selected_course_id else Subject.objects.none()
    students = Student.objects.filter(course__id=selected_course_id) if selected_course_id else Student.objects.none()

    results = []
    if selected_course_id and selected_subject_id:
        results = StudentResult.objects.filter(
            student__in=students,
            subject__id=selected_subject_id
        ).select_related('student__admin', 'subject', 'subjectmaster')

    context = {
        'courses': courses,
        'subjects': subjects,
        'results': results,
        'selected_course_id': selected_course_id,
        'selected_subject_id': selected_subject_id,
        'page_title' : 'Class Result(Subject-Wise)'
    }
    return render(request, "staff_template/class_wise_result_subject.html", context)
def manage_lesson_notes(request):
    staff = get_object_or_404(Staff, admin=request.user)
    lesson_notes = LessonSettings.objects.filter(subject__staff=staff).select_related('subject', 'curriculam')
    context = {
        'page_title': 'Manage Lesson Notes',
        'lesson_notes': lesson_notes,
    }
    return render(request, "staff_template/manage_lesson_notes.html", context)


def edit_lesson_note(request, id):
    lesson_note = get_object_or_404(LessonSettings, id=id)
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    subject = Subject.objects.filter(staff=staff).select_related('course', 'subject').distinct()
    if request.method == 'POST':
        form = LessonSettingsForm(request.POST, request.FILES, instance=lesson_note)

        if form.is_valid():
            # Get and validate curriculam from POST
            curriculam_id = request.POST.get('subject_data2')
            try:
                curriculam = Curriculam.objects.get(id=curriculam_id)
            except Curriculam.DoesNotExist:
                messages.error(request, "Selected curriculum does not exist.")
                return redirect(request.path)

            lesson_note_obj = form.save(commit=False) 
            lesson_note_obj.subject = form.cleaned_data.get('subject') or lesson_note.subject
            lesson_note_obj.curriculam = curriculam
            lesson_note_obj.date = form.cleaned_data.get('date')
            lesson_note_obj.notes = form.cleaned_data.get('notes')
               # Handle image upload
            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                image_url = fs.url(filename)
                lesson_note_obj.image = image_url
            else:
                lesson_note_obj.image = lesson_note.image  # Keep existing image

            try:
                lesson_note_obj.save()
                messages.success(request, "Lesson note updated successfully.")
                return redirect(reverse('manage_lesson_notes'))
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Form contains errors. Please correct them.")
    else:
        form = LessonSettingsForm(instance=lesson_note)

    context = {
        'form': form,
        'page_title': 'Edit Lesson Note',
        'lesson_note': lesson_note,
        'subject_list': subjects,
        # 'curriculam_list': curriculam,
        'subjects': subject,
    }

    return render(request, "staff_template/edit_lesson_note_template.html", context)
def delete_lesson_note(request, id):
    lesson_note = get_object_or_404(LessonSettings, id=id)
    try:
        lesson_note.delete()
        messages.success(request, "Lesson note deleted successfully.")
    except Exception as e:
        messages.error(request, f"Could not delete! Error: {str(e)}")
    return redirect(reverse('manage_lesson_notes'))

def staff_bulk_result(request):
    #  qs = Course.objects.values('id','name', 'division').distinct()
    #  class_list = [f"{item['name']} {item['division']}" for item in qs]
    #  print(class_list)
     course = Course.objects.all()
     examnames = ExamtypeSettings.objects.all()
     context = {
          'courses': course,
          'examnames': examnames,
           'page_title': 'Result Bulk Upload',
     }
     
     return render(request, 'staff_template/result_bulk_upload_template.html', context)

def staff_bulk_result_new(request):
     course = Course.objects.all()
     examnames = ExamtypeSettings.objects.all()
     staff = Staff.objects.get(admin=request.user)
     sessions = Session.objects.filter(
        is_active=True
    ).first()
    #  print("Staff Permission Level:", staff.permission)
     if staff.permission == 1:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('staff_home')  # or your home page
     context = {
          'courses': course,
          'examnames': examnames,
          'sessions': sessions,
           'page_title': 'Result Bulk Upload',
     }
     
     return render(request, 'staff_template/result_bulk_uploadnew_template.html', context)

def get_term_list(request):
    exam_name = request.POST.get('exam_name')
    examtype = ExamtypeSettings.objects.get(id=exam_name)
    term_list = examtype.term.split(",")  # Assuming CSV string
    term_select = [{'id': i + 1, 'name': term.strip()} for i, term in enumerate(term_list)]
    return JsonResponse(term_select, safe=False)
@csrf_exempt
def get_students_bulk(request):
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
         return JsonResponse(json.dumps(bulk_data_list),content_type='application/json', safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# @csrf_exempt
# @require_POST
# def save_student_results(request):
  
#     try:
#         data = json.loads(request.body)
#         updated_count = 0
#         created_count = 0
#         failed_entries = []

#         for entry in data:
#             try:
#                 # ----------- 1️⃣ Input Read -----------
#                 student_id = entry.get('student_id')
#                 subject_id = entry.get('subject_id')
#                 test_score = entry.get('test', 0)
#                 exam_score = entry.get('exam', 0)
#                 semester_score = entry.get('semester', 0)
#                 remarks = entry.get('remarks', '').strip()
#                 term = entry.get('term')
#                 exam_type_id = entry.get('exam_type')
#                 course_id = entry.get('course')

              

#                 # ----------- 2️⃣ Basic Validation -----------
#                 if not all([student_id, subject_id, term, exam_type_id, course_id]):
#                     failed_entries.append(f"Missing data for entry: {entry}")
#                     continue

#                 # ----------- 3️⃣ Skip fully empty rows -----------
#                 if test_score == 0 and exam_score == 0 and semester_score == 0 and not remarks:
#                     continue

#                 # ----------- 4️⃣ Ensure scores are floats -----------
#                 try:
#                     test_score = float(test_score)
#                     exam_score = float(exam_score)
#                     semester_score = float(semester_score)
#                 except ValueError:
#                     failed_entries.append(f"Invalid score for student {student_id}: {entry}")
#                     continue

#                 # ----------- 5️⃣ Validate score count -----------
#                 non_zero_score_count = sum([
#                     1 if test_score > 0 else 0,
#                     1 if exam_score > 0 else 0,
#                     1 if semester_score > 0 else 0
#                 ])

#                 if non_zero_score_count == 0:
#                     # If no score provided but remarks present, mark as Absent
#                     if not remarks:
#                         remarks = "Absent"

#                 elif non_zero_score_count > 1:
#                     failed_entries.append(
#                         f"Multiple score types entered for student {student_id}. Only one allowed. Entry: {entry}"
#                     )
#                     continue

#                 # ----------- 6️⃣ Fetch Required Objects -----------

#                 student = get_object_or_404(Student, id=student_id)
               
#                 # Important: subject_id here is the `id` of Subject table → confirmed in your table.
#                 subject_obj = get_object_or_404(Subject, course_id=course_id, subject_id=subject_id)
              
#                 exam = get_object_or_404(ExamtypeSettings, exam_name=exam_type_id)
               
#                 # If you have subjectmaster field in StudentResult model:
#                 subject_master_name = subject_obj.subject  # Adjust if field name different

#                 # ----------- 7️⃣ Save or Update StudentResult -----------
#                 result_obj, created = StudentResult.objects.update_or_create(
#                     student=student,
#                     subject=subject_obj,
#                     exam_type=exam,
#                     term=term,
#                     defaults={
#                         'subjectmaster': subject_master_name,  # Remove if field doesn't exist
#                         'test': test_score,
#                         'exam': exam_score,
#                         'semester': semester_score,
#                         'remarks': remarks or "Absent"
#                     }
#                 )

#                 if created:
#                     created_count += 1
#                 else:
#                     updated_count += 1

#             except Exception as e:
#                 # Capture exception per entry, don't stop full process
#                 failed_entries.append(f"Error for student {entry.get('student_id')}: {str(e)}")
#                 continue

#         # ----------- 8️⃣ Final Response -----------
#         total_processed = created_count + updated_count

#         if total_processed > 0:
#             message = f"{created_count} inserted, {updated_count} updated."
#             status = "success"
#         else:
#             message = "No data saved."
#             status = "empty"
#             message = "No results saved."
#         # else:
#         #     status = "success"
#         #     message = f"{created_count} created, {updated_count} updated."

#         print(f"Total created: {created_count}, updated: {updated_count}")
#         # print(f"Failed entries: {failed}")

#         return JsonResponse({
#             "status": status,
#             "message": message,
#             "failures": failed_entries  # Helpful to debug if you uncomment this
#         })

#     except Exception as e:
#         # Overall error handler
#         print("Error during result save:")
#         print(traceback.format_exc())
#         return JsonResponse({
#             "status": "error",
#             "message": str(e)
#         })
@csrf_exempt
@require_POST
def save_student_results(request):
    print("Received request to save student results.")

    try:
        staff = Staff.objects.get(admin_id=request.user.id)

        if staff.permission == 1:
            return JsonResponse({
                "status": "denied",
                "message": "Permission denied."
            }, status=403)

        data = json.loads(request.body or "[]")
        if not isinstance(data, list):
            return JsonResponse({
                "status": "error",
                "message": "Expected a JSON array of result entries."
            }, status=400)

        created_count = 0
        updated_count = 0
        failed = []
        active_session = Session.objects.filter(is_active=True).first()

        for entry in data:
            try:
                print("Processing:", entry)

                student_id = entry.get("student_id")
                subject_id = entry.get("subject_id")
                course_id = entry.get("course")
                session_id = entry.get("session")

                test_score = str(entry.get("test", "0"))
                exam_score = str(entry.get("exam", "0"))
                semester_score = str(entry.get("semester", "0"))

                remarks = str(entry.get("remarks", "")).strip()
                term = str(entry.get("term", "")).strip()
                exam_type_code = str(entry.get("exam_type", "")).strip()

                if not student_id or not subject_id or not course_id or not term or not exam_type_code:
                    failed.append(f"Missing required data for entry: {entry}")
                    continue

                if test_score == "0" and exam_score == "0" and semester_score == "0" and remarks in ["", "Absent"]:
                    print("Skipping empty student row", entry)
                    continue

                student = Student.objects.get(id=int(student_id))
                print("Student OK")

                subject = Subject.objects.get(
                    id=int(subject_id),
                    course_id=int(course_id)
                )
                print("Subject OK")

                if session_id:
                    session = Session.objects.get(id=int(session_id))
                else:
                    session = active_session

                if not session:
                    failed.append(f"No session available for entry: {entry}")
                    continue

                print("Session OK")

                exam = ExamtypeSettings.objects.get(
                    exam_name__iexact=exam_type_code
                )
                print("Exam OK")

                match_kwargs = {
                    "student": student,
                    "subject": subject,
                    "exam_type": exam,
                    "term": term,
                    "session": session,
                }
                defaults = {
                    "subjectmaster": subject.subject,
                    "test": test_score,
                    "exam": exam_score,
                    "semester": semester_score,
                    "remarks": remarks if remarks else "Absent",
                }

                existing_qs = StudentResult.objects.filter(**match_kwargs)
                if existing_qs.exists():
                    result = existing_qs.first()
                    for key, value in defaults.items():
                        setattr(result, key, value)
                    result.save()
                    created = False
                else:
                    result = StudentResult.objects.create(**match_kwargs, **defaults)
                    created = True

                print("Saved:", result.id)

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception:
                traceback.print_exc()
                failed.append(traceback.format_exc())

        response_status = "success" if created_count + updated_count > 0 else "empty"
        return JsonResponse({
            "status": response_status,
            "message": f"{created_count} created, {updated_count} updated.",
            "failures": failed
        })

    except Staff.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Staff record not found for the current user."
        }, status=400)
    except Exception:
        traceback.print_exc()
        return JsonResponse({
            "status": "error",
            "message": traceback.format_exc()
        }, status=500)
def staff_manage_bulk_result(request):

    course = Course.objects.all()
    examnames = ExamtypeSettings.objects.all()
  
    context = {
         'courses': course,
          'examnames': examnames,
        'page_title': 'Manage Bulk Result',
    }
    return render(request, 'staff_template/manage_bulk_result.html', context)


def staff_manage_bulk_result_new(request):

    course = Course.objects.all()
    examnames = ExamtypeSettings.objects.all()
    staff = Staff.objects.get(admin=request.user)
    sessions = Session.objects.filter(
        is_active=True
    ).first()
    #  print("Staff Permission Level:", staff.permission)
    if staff.permission == 1:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('staff_home')  # or your home page
    context = {
         'courses': course,
          'examnames': examnames,
        'page_title': 'Manage Bulk Result',
         'sessions': sessions
    }
    return render(request, 'staff_template/manage_bulk_resultnew.html', context)



def staff_bulk_student_data(request):
    course = request.POST.get('course')
    subject_data1 = request.POST.get('subject')
    term_wise = request.POST.get('term')
    exam_type = request.POST.get('exam')
    session = request.POST.get('session')
 
    try:
        course_obj = get_object_or_404(Course, id=course)
        subject_obj = get_object_or_404(Subject, id=subject_data1)
        examtype_obj = get_object_or_404(ExamtypeSettings, id=exam_type)
        session_obj = get_object_or_404(Session, id=session)
       
        results=StudentResult.objects.filter(
    subject_id=subject_obj.id,
    term=term_wise,
    exam_type_id=examtype_obj.id,
    student__course_id=course_obj.id,
    session_id=session_obj.id
   

)
        print(results)
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

def staff_edit_bulkresult(request, result_id):
       # ✅ Step 1: Check staff permission
    try:
        staff = Staff.objects.get(admin=request.user)
        if staff.permission:  # permission == True (1)
            # messages.error(request, "Permission denied. You are not allowed to update results.")
            return redirect('staff_manage_bulk_result_new')
    except Staff.DoesNotExist:
        messages.error(request, "Staff record not found for this user.")
        return redirect('staff_manage_bulk_result_new')
    instance = get_object_or_404(StudentResult, id=result_id)

    # Get max_marks from ExamtypeSettings
    exam_setting = ExamtypeSettings.objects.filter(
        exam_name=instance.exam_type.exam_name,
        # exam_type=instance.exam_type,
        term=instance.term
    ).first()
    session = Session.objects.filter(is_active=True).first()
    max_marks = exam_setting.max_marks if exam_setting else 20

    context = {
        'page_title': 'Edit BulkResult',
        'result': instance,
        'max_marks': max_marks,
        'courses': Course.objects.all(),
        'subjects': Subject.objects.all(),
        'sessions': session,
        'examnames': ExamtypeSettings.objects.all()
    }
    return render(request, 'staff_template/edit_bulk_result.html', context)


@csrf_exempt
def get_course_list(request):
#     course_id = request.POST.get('course')
#     # subject_names = Subject.objects.filter(course_id=course_id)
#     subject_names = Subjectmaster.objects.filter(
#     subject__course_id=course_id
# ).distinct()
#     print(subject_names)
#     subject_data_value = []
#     for subject_name in subject_names:
#         data = {
#                  "id": subject_name.id,
#                  "name": subject_name.name,
#                  "staff": subject_name.staff.admin.first_name + " " + subject_name.staff.admin.last_name if subject_name.staff.admin else "Not Assigned"
#                 }
        
#         subject_data_value.append(data) 
#     return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)
    course_id = request.POST.get('course')
    subject_names = Subject.objects.filter(course_id=course_id)
    subject_data_value = []
    for subject_name in subject_names:
        data = {
                 "id": subject_name.id,
                 "name": subject_name.subject.name,
                 "staff": (subject_name.staff.admin.first_name + " " + subject_name.staff.admin.last_name) if (subject_name.staff and subject_name.staff.admin) else "Not Assigned"
                }
        subject_data_value.append(data) 
    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)

def update_student_result(request, result_id):
    result = get_object_or_404(StudentResult, pk=result_id)

    # ✅ Step 1: Check permission before processing
    try:
        staff = Staff.objects.get(admin=request.user)
        if staff.permission:  # permission == True (1)
            # messages.error(request, "Permission denied. You are not allowed to update results.")
            return redirect('staff_manage_bulk_result_new')
    except Staff.DoesNotExist:
        messages.error(request, "Staff record not found for this user.")
        return redirect('staff_manage_bulk_result_new')

    # ✅ Step 2: Continue only if permission == False (0)
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

            if exam_name:
                test = request.POST.get('score')
            else:
                messages.error(request, "Invalid exam type.")
                return redirect(request.path)

            # ✅ Update result object
            result.student.course_id = course_id
            result.subject_id = subject_id
            result.exam_type_id = exam_type_id
            result.term = term
            result.test = test
            result.remarks = remarks
            result.save()

            messages.success(request, "Result updated successfully.")
            return redirect('staff_manage_bulk_result_new')

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
    return render(request, "staff_template/edit_bulk_result.html", context)

def delete_bulkresult(request,result_id):
    try:
        # ✅ Step 1: Check staff permission
        staff = Staff.objects.get(admin=request.user)
        if staff.permission:  # permission == True (1)
            # messages.error(request, "Permission denied. You are not allowed to delete or clear results.")
            return redirect('staff_manage_bulk_result_new')
    except Staff.DoesNotExist:
        messages.error(request, "Staff record not found for this user.")
        return redirect('staff_manage_bulk_result_new')

    # ✅ Step 2: Continue only if permission == False (0)
    result = get_object_or_404(StudentResult, id=result_id)
    
    # Clear only the marks (fields might differ based on your model)
    result.test = 0
    result.exam = 0
    result.semester = 0
    result.remarks = ""
    result.save()

    messages.success(request, "Marks cleared successfully.")
    return redirect('staff_manage_bulk_result_new')

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
    selected_course = selected_term = selected_exam = selected_exam_name = ''
    student_data = defaultdict(lambda: {
        "marks": {},
        "percentage": 0,
        "name": ""
    })
    all_subjects = set()
    results = []

    if request.GET.get("course") and request.GET.get("term") and request.GET.get("exam"):
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
            session_id=session_id,
            term=term
        ).select_related('student', 'subject', 'exam_type')

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
        'results': results,
        'sessions': sessions
    }

    return render(request, 'staff_template/class_wise_result_view.html', context_data)


@csrf_exempt  # If you're not using csrf_token properly
def get_exams_by_term(request):
    if request.method == "POST":
        term = request.POST.get("term")
        exams_qs = ExamtypeSettings.objects.filter(term=term).values("id", "exam_name")
        
        exams = list(exams_qs)  # Convert queryset to list of dicts

        return JsonResponse(exams, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)



def new_class_result(request):

    
    courses = Course.objects.all()
    subjects = Subject.objects.none()
    selected_course = request.GET.get('course')
    selected_subject = request.GET.get('subject')
    all_data = []
    session = Session.objects.filter(is_active=True).first()
    exam_columns = []
    staff = []

    if selected_course:
        subjects = Subject.objects.filter(course_id=selected_course)
#         subjects = Subjectmaster.objects.filter(
#      subject__course_id=selected_course
# ).distinct()
        # print("Fetched subjects:", subjects)
        if selected_subject:
            selected_subject = int(selected_subject)
            students = Student.objects.filter(course_id=selected_course,)

            # ✅ Fetch dynamic exam names
            exam_columns_qs = ExamtypeSettings.objects.all().order_by('id')
            exam_columns = [e.exam_name.strip().upper() for e in exam_columns_qs]

            results_qs = StudentResult.objects.filter(
                student__in=students,
                subject__id=selected_subject,
                session=session
            ).select_related('student__admin', 'exam_type')
            # print("Fetched results:", results_qs)
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
        'staff': staff,
        'sessions': session,
        'page_title': "Subjectwise Result"
    }


    return render(request, 'staff_template/classwise_result.html', context)
def staff_studentexamgraph(request):
   courses = Course.objects.all()
   exams= ExamtypeSettings.objects.all()
   session = Session.objects.filter(is_active=True).first()
   context = {
       "page_title": "Student Exam Wise Graph",
       "exams": exams,
       "courses": courses,
       "sessions": session,
   }
   return render(request, "staff_template/staff_studentexamgraph.html", context)

def staff_studentgraph(request):
    courses = Course.objects.all() 
    sessions = Session.objects.filter(is_active=True).first()
    context ={
        "page_title":"Student Graphwise",
         "courses":courses,
         "sessions":sessions,
    }
    return render(request, "staff_template/staff_studentgraph.html", context)

def get_studentmarks1(request):
    student_id = request.GET.get('student_id')
    subject_id = request.GET.get('subject_id')
    course_id = request.GET.get('course_id')
    session_id = request.GET.get('session_id')  # Assuming you have session_id in your request
    subject = Subject.objects.get(subject_id=subject_id, course_id=course_id)

    results = StudentResult.objects.filter(
        student_id=student_id,
        subject_id=subject.id,
        session_id=session_id  # Assuming ExamtypeSettings has a session_id field
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

def get_subject(request):
    course_id = request.POST.get('course')
    # print(course_id)
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
            "id": subject.subject_id,
            "name": subject.subject.name
        })
    # print(subject_data_value)
    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)
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

def get_student_marks(request):
#     student_id = request.GET.get('student_id')
#     subject_id = request.GET.get('subject_id')

#     course_id = request.GET.get('course_id')
#     # print(student_id, subject_id, course_id)
#     # try:
#     subject = Subject.objects.get(subject_id=subject_id, course_id=course_id)
#     print(subject.id)
#     # except Subject.DoesNotExist:
#         # return JsonResponse({"results": []})
#     # print("subject", subject)
#     results = StudentResult.objects.filter(
#         student_id=student_id,
#         subject_id=subject.id
#     ).select_related('exam_type')
#     # print("results", results)



#     # Sorting logic

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

#     data = []
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
#                 data.append({
#                     "exam_name": exam_name,
#                     # "exam_type": exam_type,  # like 'test paper', 'periodic test', 'semester'
#                     "marks": marks
#                 })
#             except ValueError:

#                 marks = None

#         data_list.append({
#     "exam_name": exam_name,
#     "marks": marks,
#     "exam_type": result.exam_type.id,
#     "exam_type_name": result.exam_type.exam_name  # <-- add this
# })
#     print(data_list)
#     return JsonResponse({"results": data_list})
    student_id = request.GET.get('student_id')
    subject_id = request.GET.get('subject_id')
    course_id = request.GET.get('course_id')

    subject = Subject.objects.get(subject_id=subject_id, course_id=course_id)

    results = StudentResult.objects.filter(
        student_id=student_id,
        subject_id=subject.id
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

def staff_studentexamgraph(request):
    courses = Course.objects.all()
    exams= ExamtypeSettings.objects.all()
    session = Session.objects.filter(is_active=True).first()
    context = {
        "page_title": "Student Exam Wise Graph",
        "exams": exams,
        "courses": courses,
        "sessions": session,
    }
    return render(request, 'staff_template/staff_studentexamgraph.html', context)
def get_student_bargraph(request):
    student_id = request.GET.get('student_id')
    exam_id = request.GET.get('subject_id')  # exam_type_id
    session_id = request.GET.get('session_id')
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

    return JsonResponse({'data': subject_marks, 'max_mark': max_mark})

def staff_add_result_new(request):
    staff = get_object_or_404(Staff, admin=request.user)
    print("Staff:", staff)

    # Fetch subjects and sessions
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject').distinct()
    print("Subjects:", subjects.values_list('id', flat=True))
    sessions = Session.objects.all()
    examnames = ExamtypeSettings.objects.all()

    # Fetch existing student results for this staff
    subjects_data = StudentResult.objects.select_related('subject').filter(subject__staff=staff.id)
    print("Subjects Data:", subjects_data)

    # Get all distinct courses taught by this staff through related subjects
    data_list = Course.objects.filter(subject__staff_id=staff.id).distinct()

    # Prepare context
    context = {
        'page_title': 'Result Upload',
         'subjects': subjects,
        'sessions': sessions,
        'examnames': examnames,
        'data_list': data_list,
    }

    # Handle form POST
    if request.method == "POST":
        try:
            student_id = request.POST.get("student_list")
            subject_id = request.POST.get("subject_data1")  # This is subject master id (subject.subject_id)
            exam_name_id = request.POST.get("exam_name")
            term = request.POST.get("term")
            remarks = request.POST.get("remarks")
            course_id = request.POST.get("course1")

            print("Received data:", student_id, subject_id, exam_name_id, term, remarks, course_id)

            # Score input
            score = request.POST.get("score")
            try:
                score = float(score) if score else 0
            except ValueError:
                score = 0

            # Fetch main_app_subject table record (Subject model)
            sub = get_object_or_404(
                Subject,
                staff=staff,
                course_id=course_id,
                subject_id=subject_id
            )

            subjectmaster = sub.subject  # subject master id
            print("Subject master:", subjectmaster)

            # Fetch student instance
            student = get_object_or_404(Student, id=student_id)

            # Fetch exam instance
            exam = get_object_or_404(ExamtypeSettings, id=exam_name_id)

            # Update or create student result
            result, created = StudentResult.objects.update_or_create(
                student=student,
                subject_id=sub.id,  # 💥 Corrected: use main_app_subject table id
                exam_type=exam,
                term=term,
                defaults={
                    'subjectmaster': subjectmaster,  # keep this if your model has subjectmaster field
                    'remarks': remarks or "Absent",
                    'test': score,
                }
            )

            print("Result object:", result)

            message = "Result inserted successfully." if created else "Result updated successfully."

            return render(request, "staff_template/staff_add_result_new.html", {
                "success": True,
                "message": message,
                **context
            })

        except Exception as e:
            import traceback
            print("Error during result save:")
            print(traceback.format_exc())  # Full traceback for debug

            return render(request, "staff_template/staff_add_result_new.html", {
                "error": f"Error: {str(e)}",
                **context
            })

    # GET request fallback
    return render(request, "staff_template/staff_add_result_new.html", context)
@csrf_exempt
def get_students_result(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        course_id = request.POST.get('course')
        subject_id = request.POST.get('subject')
        session_id = request.POST.get('session')
        exam_type_id = request.POST.get('exam_type')  # <-- added
       
        if not all([course_id, subject_id, session_id, exam_type_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        course = get_object_or_404(Course, id=course_id)
      
        # ✅ Get max_marks from ExamtypeSettings for this subject & exam
        exam_setting = ExamtypeSettings.objects.filter( id=exam_type_id).first()
        max_marks = exam_setting.max_marks if exam_setting else 20  # fallback to 20
        print("Max marks:", max_marks)
        # ✅ Filter students by course
        students = Student.objects.filter(course_id=course)

        student_data = []
        for student in students:
            student_data.append({
                "id": student.id,
                "name": f"{student.admin.first_name} {student.admin.last_name}",
                "max_marks": max_marks
            })
        
        return JsonResponse(student_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def get_max_marks(request):
    exam_id = request.GET.get('exam_id')
    try:
        exam = ExamtypeSettings.objects.get(id=exam_id)
        return JsonResponse({'max_marks': exam.max_marks})
    except ExamtypeSettings.DoesNotExist:
        return JsonResponse({'error': 'Invalid Exam ID'}, status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_type_colors(request):
    print("User:", request.user)
    exam_types = ExamtypeSettings.objects.values('exam_type', 'exam_name').distinct()
    
    data = {}
    for item in exam_types:
        data[item['exam_type'].lower()] = item['exam_name']  # You can also include colors here if stored
    return JsonResponse(data)  

def staff_studentexamreport(request):
    context = {
        "page_title": "Student Exam Report",
        "exams": ExamtypeSettings.objects.all(),
        "courses": Course.objects.all(),
        "subjects": Subject.objects.all(),
        "sessions": Session.objects.filter(is_active=True).first(),
    }
    return render(request, "staff_template/student_exam_report.html", context)
def _to_float(v):
    try:
        return float(v) if v not in (None, "", "NULL") else None
    except:
        return None

    
def grade_and_remark(mark, max_marks):
    if mark is None:
        return ("A", "Absent")
    pct = (mark / max_marks) * 100 if max_marks else 0
    if pct >= 95: return ("O", "Outstanding")
    if pct >= 90: return ("E", "Excellent")
    if pct >= 85: return ("VG", "Very Good")
    if pct >= 80: return ("G", "Good")
    if pct >= 70: return ("S", "Satisfactory")
    if pct >= 60: return ("A", "Average")
    if pct >= 50: return ("BA", "Below Average")
    return ("NI", "Need Improvement")


def generate_student_report_pdf(request, student_id, exam_type_id):
    student = Student.objects.select_related("course").get(id=student_id)
    user = CustomUser.objects.get(id=student.admin_id)
    session = Session.objects.filter(is_active=True).first()
    school = School.objects.first()
    exam_type = ExamtypeSettings.objects.get(id=exam_type_id)

    results = (
        StudentResult.objects
        .filter(student_id=student_id, exam_type_id=exam_type_id,session_id=session.id)
        .select_related("subject", "exam_type")
        .order_by("subject__subject__name")
    )

    rows, obtained_total, max_total = [], 0.0, 0
    hindi_malayalam = []
    other_subjects = []
    for r in results:
        subject_name = r.subject.subject.name
        max_marks = exam_type.max_marks or 100
        if exam_type.exam_name.lower():
            mark = _to_float(r.test)
        else:
            mark = None

        entry = {
            "subject": subject_name,
            "max": max_marks,
            "mark": mark if mark is not None else "-",
            "grade": grade_and_remark(mark if mark else 0, max_marks)[0],
            "remark": grade_and_remark(mark if mark else 0, max_marks)[1],
            "_raw_mark": mark
        }
        if subject_name.strip().lower() in ["hindi", "malayalam"]:
            hindi_malayalam.append(entry)
        else:
            other_subjects.append(entry)

    # Logic: among Hindi/Malayalam, show only the one with non-zero mark (if both have marks, show both)
    for entry in hindi_malayalam:
        # If both present, only show those with mark > 0
        if entry["_raw_mark"] not in [None, 0, "", "-"]:
            rows.append({k: v for k, v in entry.items() if not k.startswith('_')})
            if entry["_raw_mark"] is not None:
                obtained_total += entry["_raw_mark"]
            max_total += entry["max"]

    for entry in other_subjects:
        rows.append({k: v for k, v in entry.items() if not k.startswith('_')})
        if entry["_raw_mark"] is not None:
            obtained_total += entry["_raw_mark"]
        max_total += entry["max"]

    overall_pct = round((obtained_total / max_total) * 100, 2) if max_total else 0

    # ✅ Correct way to build file:// URIs
    school_logo = None
    if school and school.image:
        school_logo = pathlib.Path(
            os.path.join(settings.MEDIA_ROOT, school.image.name)
        ).as_uri()

    student_photo = pathlib.Path(
    os.path.join(settings.MEDIA_ROOT, user.profile_pic.name)
).as_uri()
    print(student_photo)
    context = {
        "school": school,
        "student": student,
        "course": student.course,
        "report_date": timezone.now(),
        "rows": rows,
        "obtained_total": obtained_total,
        "max_total": max_total,
        "overall_pct": overall_pct,
        "exam_name": exam_type.exam_name,
        "school_logo": school_logo,
        "student_photo": student_photo,
    }

    html = render_to_string("staff_template/report_card.html", context)

    font_css = CSS(string=f"""
        @font-face {{
            font-family: 'NotoSans';
            src: url('file://{os.path.join(settings.BASE_DIR, 'yourapp/static/fonts/NotoSans-Regular.ttf')}') format('truetype');
        }}
        body {{ font-family: 'NotoSans', sans-serif; }}
    """)

    pdf = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf(
        stylesheets=[font_css]
    )

    filename = f"Report_{student.id}_{context['exam_name']}.pdf"
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="{filename}"'
    return resp
def examtypecolors(request):
    exam_types = ExamtypeSettings.objects.values('exam_type', 'exam_name').distinct()
    
    data = {}
    for item in exam_types:
        data[item['exam_type'].lower()] = item['exam_name']  # You can also include colors here if stored
    return JsonResponse(data)
def staff_bulk_result_permissions(request):
    staff = Staff.objects.get(admin=request.user)
    print("Staff Permission Level:", staff.permission)
    if staff.permission == 1:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('staff_home')  # or your home page

    
# def add_alumini(request):
#     form = AluminiSettingsForm(request.POST or None,request.FILES or None)
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
#                 if AluminiSettings.objects.filter(email=email).exists():
#                     messages.error(request, "Student with the same email already exists.")
#                 else:
#                     # Create and save the new course
#                      alumini = AluminiSettings()
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
#                      return redirect(reverse('add_alumini'))
#             except Exception as e:
#                  messages.error(request, f"Could Not Add: {str(e)}")
#         else:
#             messages.error(request, "Please correct the following errors!")
#     return render(request,'staff_template/alumini_template.html',context)    



# ===================== LMS Views (Staff) =====================

@login_required
def staff_lms_dashboard(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    
    video_count = LMSVideo.objects.filter(subject__in=subjects).count()
    image_count = LMSImage.objects.filter(subject__in=subjects).count()
    note_count = LMSNote.objects.filter(subject__in=subjects).count()
    total_content = video_count + image_count + note_count
    
    # Per-subject content counts
    subject_data = []
    for subj in subjects:
        v = LMSVideo.objects.filter(subject=subj).count()
        i = LMSImage.objects.filter(subject=subj).count()
        n = LMSNote.objects.filter(subject=subj).count()
        subject_data.append({
            'subject': subj,
            'videos': v,
            'images': i,
            'notes': n,
            'total': v + i + n,
        })
    
    # Combined recent uploads (last 8 items)
    recent_videos = list(LMSVideo.objects.filter(
        subject__in=subjects
    ).order_by('-created_at')[:8].values(
        'id', 'title', 'subject__subject__name', 'created_at'
    ))
    for item in recent_videos:
        item['type'] = 'video'
        item['icon'] = 'fas fa-video'
        item['color_class'] = 'bg-primary'
    
    recent_images = list(LMSImage.objects.filter(
        subject__in=subjects
    ).order_by('-created_at')[:8].values(
        'id', 'title', 'subject__subject__name', 'created_at'
    ))
    for item in recent_images:
        item['type'] = 'image'
        item['icon'] = 'fas fa-image'
        item['color_class'] = 'bg-success'
    
    recent_notes = list(LMSNote.objects.filter(
        subject__in=subjects
    ).order_by('-created_at')[:8].values(
        'id', 'title', 'subject__subject__name', 'created_at'
    ))
    for item in recent_notes:
        item['type'] = 'note'
        item['icon'] = 'fas fa-sticky-note'
        item['color_class'] = 'bg-warning'
    
    all_recent = sorted(
        recent_videos + recent_images + recent_notes,
        key=lambda x: x['created_at'],
        reverse=True
    )[:8]
    
    context = {
        'page_title': 'LMS Dashboard',
        'staff': staff,
        'video_count': video_count,
        'image_count': image_count,
        'note_count': note_count,
        'total_content': total_content,
        'subject_count': subjects.count(),
        'subject_data': subject_data,
        'all_recent': all_recent,
    }
    return render(request, "staff_template/staff_lms_dashboard.html", context)


# ---------- VIDEO CRUD ----------

@login_required
def staff_add_lms_video(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    
    if request.method == 'POST':
        form = LMSVideoForm(request.POST, request.FILES)
        subject_id = request.POST.get('subject_id')
        if not subject_id:
            messages.error(request, "Please select a subject.")
        elif form.is_valid():
            try:
                # Server-side file type validation
                video_file = request.FILES.get('video')
                if video_file:
                    allowed_video_ext = ['.mp4', '.mov', '.webm', '.avi', '.mkv', '.m4v']
                    ext = os.path.splitext(video_file.name)[1].lower()
                    if ext not in allowed_video_ext:
                        messages.error(request, f"Invalid video format '{ext}'. Allowed: {', '.join(allowed_video_ext)}")
                        raise ValueError("Invalid file type")
                
                video = form.save(commit=False)
                subject = get_object_or_404(Subject, id=subject_id)
                video.subject = subject
                video.course = subject.course
                video.uploaded_by = request.user
                video.save()
                messages.success(request, "Video uploaded successfully.")
                return redirect(reverse('staff_manage_lms_videos'))
            except ValueError:
                pass  # Message already set above
            except Exception as e:
                messages.error(request, f"Error uploading video: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSVideoForm()
    
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Add Video',
        'form': form,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_add_lms_video.html", context)


@login_required
def staff_manage_lms_videos(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    videos = LMSVideo.objects.filter(subject__in=subjects).order_by('-created_at')
    
    context = {
        'page_title': 'Manage Videos',
        'videos': videos,
    }
    return render(request, "staff_template/staff_manage_lms_videos.html", context)


@login_required
def staff_view_lms_video(request, id):
    staff = get_object_or_404(Staff, admin=request.user)
    video = get_object_or_404(LMSVideo, id=id)
    
    # Enforce staff viewing their own videos/subjects
    if video.subject.staff != staff:
        messages.error(request, "You do not have permission to view this video.")
        return redirect(reverse('staff_manage_lms_videos'))
        
    next_videos = LMSVideo.objects.filter(course=video.course).exclude(id=id).order_by('-created_at')[:5]
    
    context = {
        'page_title': 'View Video',
        'video': video,
        'next_videos': next_videos,
    }
    return render(request, "staff_template/staff_view_lms_video.html", context)


@login_required
def staff_edit_lms_video(request, id):
    staff = get_object_or_404(Staff, admin=request.user)
    video = get_object_or_404(LMSVideo, id=id, uploaded_by=request.user)
    
    if request.method == 'POST':
        form = LMSVideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            try:
                # Delete old file from disk if a new one is being uploaded
                new_video_file = request.FILES.get('video')
                if new_video_file and video.video:
                    old_path = video.video.path
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                
                updated_video = form.save(commit=False)
                subject_id = request.POST.get('subject_id')
                if subject_id:
                    subject = get_object_or_404(Subject, id=subject_id)
                    updated_video.subject = subject
                    updated_video.course = subject.course
                updated_video.save()
                messages.success(request, "Video updated successfully.")
                return redirect(reverse('staff_manage_lms_videos'))
            except Exception as e:
                messages.error(request, f"Error updating video: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSVideoForm(instance=video)
    
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Edit Video',
        'form': form,
        'video': video,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_edit_lms_video.html", context)


@login_required
@require_POST
def staff_delete_lms_video(request, id):
    video = get_object_or_404(LMSVideo, id=id, uploaded_by=request.user)
    try:
        # Delete media file from disk
        if video.video and os.path.isfile(video.video.path):
            os.remove(video.video.path)
        video.delete()
        messages.success(request, "Video deleted successfully.")
    except Exception as e:
        messages.error(request, f"Could not delete video: {str(e)}")
    return redirect(reverse('staff_manage_lms_videos'))


# ---------- IMAGE CRUD ----------

@login_required
def staff_add_lms_image(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    
    if request.method == 'POST':
        form = LMSImageForm(request.POST, request.FILES)
        subject_id = request.POST.get('subject_id')
        if not subject_id:
            messages.error(request, "Please select a subject.")
        elif form.is_valid():
            try:
                # Server-side file type validation
                image_file = request.FILES.get('image')
                if image_file:
                    allowed_image_ext = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg']
                    ext = os.path.splitext(image_file.name)[1].lower()
                    if ext not in allowed_image_ext:
                        messages.error(request, f"Invalid image format '{ext}'. Allowed: {', '.join(allowed_image_ext)}")
                        raise ValueError("Invalid file type")
                
                image = form.save(commit=False)
                subject = get_object_or_404(Subject, id=subject_id)
                image.subject = subject
                image.course = subject.course
                image.uploaded_by = request.user
                image.save()
                messages.success(request, "Image uploaded successfully.")
                return redirect(reverse('staff_manage_lms_images'))
            except ValueError:
                pass  # Message already set above
            except Exception as e:
                messages.error(request, f"Error uploading image: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSImageForm()
    
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Add Image',
        'form': form,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_add_lms_image.html", context)


@login_required
def staff_manage_lms_images(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    images = LMSImage.objects.filter(subject__in=subjects).order_by('-created_at')
    
    context = {
        'page_title': 'Manage Images',
        'images': images,
    }
    return render(request, "staff_template/staff_manage_lms_images.html", context)


@login_required
def staff_edit_lms_image(request, id):
    staff = get_object_or_404(Staff, admin=request.user)
    image = get_object_or_404(LMSImage, id=id, uploaded_by=request.user)
    
    if request.method == 'POST':
        form = LMSImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            try:
                # Delete old file from disk if a new one is being uploaded
                new_image_file = request.FILES.get('image')
                if new_image_file and image.image:
                    old_path = image.image.path
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                
                updated_image = form.save(commit=False)
                subject_id = request.POST.get('subject_id')
                if subject_id:
                    subject = get_object_or_404(Subject, id=subject_id)
                    updated_image.subject = subject
                    updated_image.course = subject.course
                updated_image.save()
                messages.success(request, "Image updated successfully.")
                return redirect(reverse('staff_manage_lms_images'))
            except Exception as e:
                messages.error(request, f"Error updating image: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSImageForm(instance=image)
    
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Edit Image',
        'form': form,
        'image': image,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_edit_lms_image.html", context)


@login_required
@require_POST
def staff_delete_lms_image(request, id):
    image = get_object_or_404(LMSImage, id=id, uploaded_by=request.user)
    try:
        # Delete media file from disk
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)
        image.delete()
        messages.success(request, "Image deleted successfully.")
    except Exception as e:
        messages.error(request, f"Could not delete image: {str(e)}")
    return redirect(reverse('staff_manage_lms_images'))


# ---------- NOTE CRUD ----------

@login_required
def staff_add_lms_note(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    
    if request.method == 'POST':
        form = LMSNoteForm(request.POST, request.FILES)
        subject_id = request.POST.get('subject_id')
        if not subject_id:
            messages.error(request, "Please select a subject.")
        elif form.is_valid():
            try:
                # Server-side file type validation
                note_file = request.FILES.get('file')
                if note_file:
                    allowed_note_ext = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.txt']
                    ext = os.path.splitext(note_file.name)[1].lower()
                    if ext not in allowed_note_ext:
                        messages.error(request, f"Invalid file format '{ext}'. Allowed: {', '.join(allowed_note_ext)}")
                        raise ValueError("Invalid file type")
                
                note = form.save(commit=False)
                subject = get_object_or_404(Subject, id=subject_id)
                note.subject = subject
                note.course = subject.course
                note.uploaded_by = request.user
                note.save()
                messages.success(request, "Note added successfully.")
                return redirect(reverse('staff_manage_lms_notes'))
            except ValueError:
                pass  # Message already set above
            except Exception as e:
                messages.error(request, f"Error adding note: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSNoteForm()
    
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Add Note',
        'form': form,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_add_lms_note.html", context)


@login_required
def staff_manage_lms_notes(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    notes = LMSNote.objects.filter(subject__in=subjects).order_by('-created_at')
    
    context = {
        'page_title': 'Manage Notes',
        'notes': notes,
    }
    return render(request, "staff_template/staff_manage_lms_notes.html", context)


@login_required
def staff_edit_lms_note(request, id):
    staff = get_object_or_404(Staff, admin=request.user)
    note = get_object_or_404(LMSNote, id=id, uploaded_by=request.user)
    
    if request.method == 'POST':
        form = LMSNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            try:
                # Delete old file from disk if a new one is being uploaded
                new_note_file = request.FILES.get('file')
                if new_note_file and note.file:
                    old_path = note.file.path
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                
                updated_note = form.save(commit=False)
                subject_id = request.POST.get('subject_id')
                if subject_id:
                    subject = get_object_or_404(Subject, id=subject_id)
                    updated_note.subject = subject
                    updated_note.course = subject.course
                updated_note.save()
                messages.success(request, "Note updated successfully.")
                return redirect(reverse('staff_manage_lms_notes'))
            except Exception as e:
                messages.error(request, f"Error updating note: {str(e)}")
        else:
            messages.error(request, "Please fill the form properly.")
    else:
        form = LMSNoteForm(instance=note)
    
    subjects = Subject.objects.filter(staff=staff).select_related('course', 'subject')
    subject_list = []
    for subj in subjects:
        subject_list.append({
            'id': subj.id,
            'name': subj.subject.name,
            'course': subj.course.name if subj.course else "",
            'division': subj.course.division if subj.course else "",
        })
    subject_list = sorted(subject_list, key=lambda x: (x['course'], x['name']))
    
    context = {
        'page_title': 'Edit Note',
        'form': form,
        'note': note,
        'subject_list': subject_list,
    }
    return render(request, "staff_template/staff_edit_lms_note.html", context)


@login_required
@require_POST
def staff_delete_lms_note(request, id):
    note = get_object_or_404(LMSNote, id=id, uploaded_by=request.user)
    try:
        # Delete media file from disk
        if note.file and os.path.isfile(note.file.path):
            os.remove(note.file.path)
        note.delete()
        messages.success(request, "Note deleted successfully.")
    except Exception as e:
        messages.error(request, f"Could not delete note: {str(e)}")
    return redirect(reverse('staff_manage_lms_notes'))
