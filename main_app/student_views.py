import json
import math
from datetime import datetime
import re
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
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
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

import os
def get_attendance_data(student):
    """Retrieve attendance data for the student."""
    total_attendance = AttendanceReport.objects.filter(student=student).count()
    total_present = AttendanceReport.objects.filter(student=student, status=True).count()

    if total_attendance == 0:  # Avoid DivisionByZero
        percent_present = percent_absent = 0
    else:
        percent_present = math.floor((total_present / total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)

    return total_attendance, percent_present, percent_absent

def get_subject_attendance(student, subjects):
    """Retrieve attendance data for each subject."""
    subject_names = []
    data_present = []
    data_absent = []
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, student=student
        ).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, student=student
        ).count()
        subject_names.append(subject.subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    return subject_names, data_present, data_absent

def get_exam_results(student, subjects):
    """Retrieve exam results, top marks, and averages."""
    results = StudentResult.objects.filter(student_id=student.id)
    # Data for graphs
    subjects_graph_data = []
    marks_graph_data = []
    for result in results:
        subjects_graph_data.append(result.subject.subject.name)
        marks_graph_data.append(result.exam)
    # Top marks and averages
    # Lists to store the results
    top_marks = []
    subject_averages = []
# Assuming terms is a predefined list of terms like ['Term1', 'Term2', 'Term3']
    terms = ['Term-3', 'Term-2', 'Term-1']
    subject_top_marks = []
    subject_term_averages = []
# Outer loop for subjects
    for subject in subjects: 
    # Inner loop for terms
     for term in terms:
        # Get the top mark for the current subject and term
        top_mark = StudentResult.objects.filter(subject_id=subject.subject_id, term=term).order_by('-exam').first()
        # print(top_mark)
        # Get the average mark for the current subject and term
        avg_mark = (
            StudentResult.objects.filter(subject_id=subject.subject_id, term=term)
            .aggregate(Avg('exam'))['exam__avg']
        )

        # Append the top mark and average for this term
        subject_top_marks.append(top_mark.exam if top_mark else 0)
        subject_term_averages.append(avg_mark if avg_mark is not None else 0)

    # Store the results for the current subject
    top_marks.append(subject_top_marks)
    subject_averages.append(subject_term_averages)
    return subjects_graph_data, marks_graph_data, top_marks, subject_averages


def get_term_wise_data(student, subjects):
    """Retrieve term-wise marks for each subject."""
    term_wise_marks_data = {}

    for subject in subjects:
        terms = StudentResult.objects.filter( student=student, subject_id=subject.subject_id ).values_list('term', flat=True).distinct()
        term_marks = []
        term_labels = []

        for term in terms:
            marks = StudentResult.objects.filter(
                student=student, subject_id=subject.subject_id, term=term
            ).first()
            if marks:
                term_marks.append(marks.exam)
                term_labels.append(term)
        
        term_wise_marks_data[subject.subject.name] = {
            "terms": term_labels,
            "marks": term_marks
        }
    
    # Return the full dictionary after processing all subjects
    return term_wise_marks_data

def student_home(request):
    """Student dashboard view."""
    student = get_object_or_404(Student, admin=request.user)
    subjects = Subject.objects.filter(course=student.course)

    # Attendance Data
    total_attendance, percent_present, percent_absent = get_attendance_data(student)
    subject_names, data_present, data_absent = get_subject_attendance(student, subjects)

    # Exam Results
    subjects_graph_data, marks_graph_data, top_marks, subject_averages = get_exam_results(student, subjects)

    # Term-wise Marks
    term_wise_marks_data = get_term_wise_data(student, subjects)

    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': subjects.count(),
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_names,
        'subject_graph_data': subjects_graph_data,
        'marks_graph_data': marks_graph_data,
        'top_marks': top_marks[0],
        'avg_marks': subject_averages[0],
        'term_wise_marks_data': term_wise_marks_data,
        'page_title': 'Student Homepage',
    }
   
    return render(request, 'student_template/home_content.html', context)


@ csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(Student, admin=request.user)
    if request.method != 'POST':
        course = get_object_or_404(Course, id=student.course.id)
        context = {
            'subjects': Subject.objects.filter(course=course),
            'page_title': 'View Attendance'
        }
        return render(request, 'student_template/student_view_attendance.html', context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, student=student)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None
        
def student_apply_leave(request):
    student = get_object_or_404(Student, admin_id=request.user.id)
    form = LeaveReportStudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            leave_report = form.save(commit=False)
            leave_report.student = student
            if 'image' in request.FILES:
                leave_report.image = request.FILES['image']
            leave_report.save()
            messages.success(request, "Leave application submitted successfully.")
            return redirect(reverse('student_apply_leave'))
        else:
            messages.error(request, "Form has errors!")
    context = {
        'form': form,
        'leave_history': LeaveReportStudent.objects.filter(student=student),
        'page_title': 'Apply for leave'
    }
    return render(request, "student_template/student_apply_leave.html", context)

def edit_student_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveReportStudent, id=leave_id, student__admin_id=request.user.id)
    form = LeaveReportStudentForm(request.POST or None, instance=leave_request)
    context = {
        'form': form,
        'leave_history': LeaveReportStudent.objects.filter(student=leave_request.student),
        'page_title': 'Edit Leave Request'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Leave request has been updated")
                return redirect(reverse('student_apply_leave'))
            except Exception:
                messages.error(request, "Could not update leave request")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student_template/edit_student_leave_template.html", context)

def delete_student_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveReportStudent, id=leave_id, student__admin_id=request.user.id)
    try:
        leave_request.delete()
        messages.success(request, "Leave request has been deleted")
    except Exception:
        messages.error(request, "Could not delete leave request")
    return redirect(reverse('student_apply_leave'))



def student_feedback(request):
    form = FeedbackStudentForm(request.POST or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStudent.objects.filter(student=student),
        'page_title': 'Student Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('student_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student_template/student_feedback.html", context)


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                gender = form.cleaned_data.get('gender')
                house_name = form.cleaned_data.get('house_name')
                place_name = form.cleaned_data.get('place_name')
                district_name =form.cleaned_data.get('district_name')
                city = form.cleaned_data.get('city')
                course = form.cleaned_data.get('course')
                session = form.cleaned_data.get('session')
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                admission_number = form.cleaned_data.get('admission_number')
                parent_name = form.cleaned_data.get('parent_name')
                mother_tongue =form.cleaned_data.get('mother_tongue')
                date_of_birth=form.cleaned_data['date_of_birth']
                passport = request.FILES.get('profile_pic') or None
                admin = student.admin
                if password != None:
                    admin.set_password(password)
                admin.first_name = first_name
                admin.last_name = last_name
                admin.house_name = house_name
                admin.place_name = place_name
                admin.district_name = district_name
                admin.admission_number = admission_number
                admin.parent_name = parent_name
                admin.mother_tongue= mother_tongue
                admin.date_of_birth = date_of_birth
                admin.street_address = street_address
                admin.course = course
                admin.city = city
                admin.country = country
                admin.state = state
                admin.session = session
                admin.gender = gender
                admin.save()
                student.save()
                if passport:
                    save_user_profile_pic(passport, admin)
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "student_template/student_view_profile.html", context)


@csrf_exempt
def student_fcmtoken(request):
    token = request.POST.get('token')
    student_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        student_user.fcm_token = token
        student_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def student_view_notification(request):
    student = get_object_or_404(Student, admin=request.user)
    notifications = NotificationStudent.objects.filter(student=student)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "student_template/student_view_notification.html", context)


def student_view_result(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('term')
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "student_template/student_view_result.html", context)


def detailed_evaluation(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('term')
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "student_template/student_detailed_evaluation.html", context)

def student_view_result_preview(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('term')
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "student_template/student_result_preview.html", context)

def term_wise_list(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('term')
    context = {
        'results': results,
        'page_title': "Term Wise Results"
    }
    return render(request, "student_template/student_term_wise_list.html", context)
@csrf_exempt
def get_terms(request):
    term_name = request.POST.get('term')
    if not term_name:
        return JsonResponse({"error": "Term is required"}, status=400)

    try:
        student = get_object_or_404(Student, admin=request.user)
        results = StudentResult.objects.filter(student=student, term=term_name, )

        student_data = []
        # for subject in subjects:
        for result in results:
            data = {
                "test": result.test,
                "exam": result.exam,
                "subject_name": result.subject.subject.name,
                "remarks": result.remarks

            }
            student_data.append(data)

        # return JsonResponse(student_data, safe=False)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Http404:
        return JsonResponse({"error": "Data not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
#  ....... term wise pdf......

def generate_term_pdf(request,term_wise):
    student = get_object_or_404(Student, admin=request.user)
      # Create the HttpResponse object with the appropriate PDF headers.
    schools = School.objects.all()
    for school in schools:
        # Create a new PDF page. 
        pdf = canvas.Canvas("school.pdf")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="results.pdf"'
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    image_path = school.image
    file_path = image_path.path
    relative_image_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_image_path)    
    image_reader = ImageReader(full_path)
    x_position = width - 500
    y_position = height - 100
    p.drawImage(image_reader, x=x_position, y=y_position, width=50, height=50)
    # Draw the header
    p.setFont("Helvetica", 20)
    p.setFont("Helvetica", 20)
   
    p.drawString(160, height - 70, f'{school.name}')
    p.setFont("Helvetica", 16)
    p.drawString(180, height - 100, f'{school.address}')
    p.drawString(380, height - 100, f'{school.email}')
    p.line(100, height - 110, width - 100, height - 110)
    p.setFont("Helvetica", 14)    
        # Draw a line below the header
    p.line(100, height - 110, width - 100, height - 110)
    p.drawString(250, height - 130, "Results Report")

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 150, f'Name: {request.user.first_name + " " + request.user.last_name}')
    p.drawString(100, height - 170, f'Student ID:{student.admission_number}')
    p.drawString(250, height - 170, f'Class/Division: {student.course}')
    p.drawString(400, height - 170, f"Attendance: {get_attendance_data(student)}")
    #----------------------------------------
    p.setFont("Helvetica-Bold", 12)
    p.drawString(90, height - 200, "Subject")
    p.drawString(150, height - 200, "Total Mark")
    p.drawString(230, height - 200, "Test Mark")
    p.drawString(300, height - 200, "Exam Mark")
    p.drawString(380, height - 200, "Subject Grade")
    p.drawString(490, height - 200, "Remarks")

    # Draw a line under the table headers
   # p.line(100, height - 185, width - 100, height - 185)

    # Table Rows
    y = height - 200
    p.setFont("Helvetica", 12)

    # Draw a line above the footer
    #p.line(100, y - 10, width - 100, y - 10)

    # Footer
    p.setFont("Helvetica", 10)
    #p.drawString(180, y - 130, "Generated by the Student Results System")

    #Close the PDF object cleanly.

    #--------------------------------

    # Draw the results
    y = height - 230

    results = StudentResult.objects.filter(student=student, term=term_wise)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    for result in results:

        p.drawString(90, y, str(result.subject.subject.name))
        p.drawString(180, y,  str(100))
        p.drawString(250, y, str(result.test))
        p.drawString(330, y, str(result.exam))
        p.drawString(430, y, str("O"))
        p.drawString(510, y, str(result.remarks))
        y -= 40

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response
def student_view_curriculam(request):
    student = get_object_or_404(Student, admin=request.user)
    subjects = Subject.objects.filter(course=student.course)
    results = Curriculam.objects.select_related('course').all()
   # result=results = Student.objects.select_related('subject', 'subject__curriculam').values(
   #S 'id', 'course_id', 'subject__subject_id', 'subject__curriculam__subject_id')
    context = {
        'subjects': subjects,
        'page_title': "Curriculum",
        'results': results
    }
    return render(request, "student_template/student_view_curriculam.html", context)

def student_hpcard(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student).order_by('term')
    student_results = StudentResult.objects.filter(student=student)
    context = {
        'results': results,
        'student': student,
        'student_results':student_results,
        'page_title': "Holistic Progress Card"
    }
    return render(request, "student_template/student_hpcard.html", context)
@csrf_exempt
def student_report_hpc(request):
    student = get_object_or_404(Student, admin=request.user)
    customUser = CustomUser.objects.get(id=student.admin_id)
    school = School.objects.all()

    student_results = StudentResult.objects.filter(student=student)
    subject_data = {}

    TERM_CHOICES = ["Term-1", "Term-2", "Term-3"]

    for result in student_results:
        subject_name = result.subject.subject.name
        term = result.term

        if subject_name not in subject_data:
            subject_data[subject_name] = {
                t: {"test": 0, "exam": 0} for t in TERM_CHOICES
            }
            subject_data[subject_name]["total_test"] = 0
            subject_data[subject_name]["total_exam"] = 0
            subject_data[subject_name]["overall_total"] = 0

        # Assign marks
        subject_data[subject_name][term]["test"] = result.test
        subject_data[subject_name][term]["exam"] = result.exam

    # Compute totals **after** all results have been looped through
    for subject, terms in subject_data.items():
        total_test = 0
        total_exam = 0

        for term in TERM_CHOICES:
           total_test += float(terms[term]["test"] or 0)
           total_exam += float(terms[term]["exam"] or 0)

        subject_data[subject]["total_test"] = total_test
        subject_data[subject]["total_exam"] = total_exam
        subject_data[subject]["overall_total"] = total_test + total_exam

    context = {
        'subject_data': subject_data,
        'student': student,
        'customUser': customUser,
        'school': school,
        'page_title': "Holistic Progress Card",
    }
    return render(request, "student_template/student_hpcard_view.html", context)
