import json
from .models import Subject
from multiprocessing import context
from django.db.models import Q, F, OuterRef, Subquery, Exists
from django.db import IntegrityError, transaction
from main_app.models import Subject, Course, Subjectmaster
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from openpyxl.utils import get_column_letter
from .forms import *
from .models import *
import os
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Concat, Replace, Upper
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests
from django.templatetags.static import static
from django.views.generic import UpdateView
from openpyxl import load_workbook
from .models import Student
from .forms import AccAdminForm
from .models import CustomUser
import openpyxl
from .profile_utils import save_user_profile_pic, delete_user_profile_pic
import traceback
import pandas as pd
from .forms import ExcelUploadForm
from django.shortcuts import render
import pandas as pd
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from io import BytesIO
from .models import Student
from openpyxl.utils.dataframe import dataframe_to_rows  # Correct import
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import uuid
from collections import defaultdict
from .models import Student, StudentResult, ExamtypeSettings 
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import traceback
from collections import defaultdict
import traceback
import re
import random
from django.template.loader import render_to_string
# from weasyprint import HTML, CSS  # Commented out due to missing GTK+ libraries on Windows
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


def acc_admin_home(request):
   
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    # subjects = Subjectmaster.objects.all()
    total_subject = Subjectmaster.objects.all().count()
    total_course = Course.objects.values('name').distinct().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        # subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
        
       
    context = {
        
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'subjects':subjects,
        'courses' :courses,

    }
    return render(request, 'acc_admin_template/home_content.html',context )

def add_curriculam(request):
    form = CurriculamForm(request.POST or None)
    courses = Course.objects.all() 
    context = {
        'form': form,
        'page_title': 'Add Curriculum',
        'courses' :courses,
    }
    return render(request, 'acc_admin_template/add_crriculam_template.html',context )
    
@csrf_exempt
def get_course(request):
    course_id = request.POST.get('course')
    subject_names = Subject.objects.filter(course_id=course_id)
    subject_data = []
    for subject_name in subject_names:
        data = {
                 "id": subject_name.subject.id,
                 "name": subject_name.subject.name,
                 "staff": subject_name.staff.admin.first_name + " " + subject_name.staff.admin.last_name if subject_name.staff.admin else "Not Assigned"
                }
        subject_data.append(data) 
    return JsonResponse(json.dumps(subject_data), content_type='application/json', safe=False)

@csrf_exempt
def get_curriculam(request):
    if request.method == 'POST':
        form = CurriculamForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course')
            subject_id = request.POST.get('subject_data')
            lesson = request.POST.get('lesson')
            term = request.POST.get('term_wise')
            title = request.POST.get('title')

            try:

                # Convert to integer if necessary
                subject_obj = Subject.objects.get(subject_id=subject_id, course_id=course_id)
                actual_subject_pk = subject_obj.id  # this is the PK from main_app_subject

                if Curriculam.objects.filter(
                    lesson=lesson,
                    course_id=course_id,
                    subject_id=actual_subject_pk,
                    term=term,
                    title=title
                ).exists():
                    return JsonResponse({'status': 'error', 'message': 'Curriculum already exists.'})

                # Save with the actual subject PK
                curriculam = Curriculam(
                    lesson=lesson,
                    course_id=course_id,
                    subject_id=actual_subject_pk,
                    title=title,
                    term=term
                )
                curriculam.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Successfully Added',
                    'subject_db_id': actual_subject_pk  # show subject table's ID if needed
                })
            except Subject.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Subject not found'})

                if  Curriculam.objects.filter(lesson=lesson, course_id=course_id, subject_id=subject_id, term=term,title=title).exists():
                    return JsonResponse({'status': 'error', 'message': 'A curriculum with the same lesson, course, term,title and subject already exists.'})
                
                else:
                    sub = Subject.objects.get(course_id=course_id, subject_id=subject_id)
                    actual_subject = sub.id
                    
                    curriculam = Curriculam(lesson=lesson, course_id=course_id, subject_id=actual_subject,title=title, term=term)
                    curriculam.save()
                    return JsonResponse({'status': 'success', 'message': 'Successfully Added'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Could Not Add: {str(e)}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please fulfill all requirements'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def manage_curriculam(request):
           form = CurriculamForm(request.POST or None)
           courses = Course.objects.all() 
           curriculams = Curriculam.objects.all().order_by('term')
           context = {
                'curriculams': curriculams,
                'page_title': 'Manage Curriculum',
                'courses' :courses,
           }
           return render(request, 'acc_admin_template/manage_curriculam_template.html',context )

def edit_curriculam(request, id):
    # Fetch the existing Curriculam instance
    curriculam = get_object_or_404(Curriculam, id=id)

    # Prepopulate the form with existing instance
    form = CurriculamForm(request.POST or None, instance=curriculam)

    # Fetch related data for the form
    subjects = Subject.objects.all().distinct()
    courses = Course.objects.all()

    # Context for rendering the template
    context = {
        'form': form,
        'page_title': 'Edit Curriculum',
        'id': id,
        'curriculam': curriculam,
        'courses': courses,
        'subjects': subjects,
        'term_wise': curriculam.term
    }
    if request.method == 'POST':
        if form.is_valid():
            term = request.POST.get('term')
            course = request.POST.get('course_id')
            subject = request.POST.get('subject_data')

            # Check if all required fields are present
            if not term or not course or not subject:
                messages.error(request, "Please select Term.")
                return render(request, 'acc_admin_template/edit_curriculam_template.html', context)

            # Save the form but do not commit immediately
            curriculam = form.save(commit=False)

            # Update additional fields
            curriculam.term = term
            curriculam.course_id = course
            curriculam.subject_id = subject

            curriculam.save()  # Save changes to the database

            # Display success message
            messages.success(request, "Curriculum successfully updated!")
            return redirect('manage_curriculam')

        else:
            # Display error messages if form is invalid
            messages.error(request, "Error updating the curriculum. Please check your input.")

    return render(request, 'acc_admin_template/edit_curriculam_template.html', context)

def delete_curriculam(request, id):
       curriculam = Curriculam.objects.get(id=id)
       curriculam.delete()
       messages.success(request, "Successfully Deleted")
       return redirect(reverse('manage_curriculam'))
@csrf_exempt
def get_teachers(request):
   course_id = request.POST.get('course')
   subject_id =request.POST.get('subject')
   teachers = Staff.objects.filter(subject__course_id=course_id, id=subject_id)
   teacher_data = []
   for teacher in teachers:
        teacher_data.append(teachers)
        return JsonResponse(json.dumps(teacher_data), content_type='application/json', safe=False)
   
def add_subject_master(request):
       form = SubjectmasterForm(request.POST or None)
       context = {'form': form, 'page_title': 'Add Subject Master'}
       if request.method == 'POST':
            if form.is_valid():
                 name = form.cleaned_data.get('name')
                 department  = form.cleaned_data.get('department')
                 try:
                     if Subjectmaster.objects.filter(name=name,department=department).exists():
                        messages.error(request, " Subject name and Department name already exists.")
                     else :  
                        subjectmaster = Subjectmaster()
                        subjectmaster.name = name
                        subjectmaster.department = department
                        subjectmaster.save()
                        messages.success(request, "Successfully Added")
                     return redirect(reverse('add_subject_master'))
                 except Exception as e:
                     messages.error(request, "Could Not Add " + str(e))
       return render(request, 'acc_admin_template/subject_master_template.html',context )

def add_department(request):
       form = DepartmentForm(request.POST or None)
       context = {'form': form, 'page_title': 'Add Department'}
       if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                if Department.objects.filter(name=name).exists():
                    messages.error(request, "Department name already exists.")
                else:
                    department = Department()
                    department.name = name
                    department.save()
                    messages.success(request, "Successfully Added")
                return redirect(reverse('add_department'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

       return render(request, 'acc_admin_template/department_template.html',context )

def manage_department(request):
     departments = Department.objects.all()
     message = request.GET.get('message', '')
     message_type = request.GET.get('message_type', '')
     context = {
          'departments': departments,
          'page_title': 'Manage Department',
          'message': message,
          'message_type': message_type
     }
     return render(request, 'acc_admin_template/manage_department_template.html',context )

def edit_department(request,id):
     department = get_object_or_404(Department,id=id)
     form = DepartmentForm(request.POST or None, instance=department)
     context = {
          'form': form,
          'page_title': 'Edit Department',
          'id': id,
          'department': department,
     }
     if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department.name = name
            department.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('manage_department'))
        else:
            messages.error(request, "Fill Form Properly")
     return render(request, 'acc_admin_template/edit_department_template.html',context )

def delete_department(request,id):
     department = get_object_or_404(Department, id=id)
     if Staff.objects.filter(department=department).exists() or Subjectmaster.objects.filter(department=department).exists():
        messages.error(request, "This department cannot be deleted as it has associated staff or subjects.")
        return redirect(reverse('manage_department'))
     else:
        department.delete()
        messages.success(request, "Successfully Deleted")
        return redirect(reverse('manage_department'))

def manage_subject_master(request):
     subjectmasters = Subjectmaster.objects.all()
     context = {
          'subjectmasters': subjectmasters,
          'page_title': 'Manage Subject Master',
     }
     return render(request, 'acc_admin_template/manage_subject_master_template.html',context )

def edit_subjectmaster(request,id):
     subjectmaster = get_object_or_404(Subjectmaster,id=id)
     form = SubjectmasterForm(request.POST or None, instance=subjectmaster)
     context = {
          'form': form,
          'page_title': 'Edit Subject Master',
          'id': id,
          'subjectmaster': subjectmaster,
     }
     if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')
            subjectmaster.name = name
            subjectmaster.department = department
            subjectmaster.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('manage_subject_master'))
        else:
            messages.error(request, "Fill Form Properly")
     return render(request, 'acc_admin_template/edit_subject_master_template.html',context)

def delete_subjectmaster(request,id):
     subjectmaster = Subjectmaster.objects.get(id=id)
     subjectmaster.delete()
     messages.success(request, "Successfully Deleted")
     return redirect(reverse('manage_subject_master'))

def academic_add_result(request):
       courses = Course.objects.all() 
       context = {
             'page_title': 'Excel Form',
              'courses' :courses,
        }
       return render(request, 'acc_admin_template/academic_add_result_template.html',context)

def academic_bulk_result(request):
    #  qs = Course.objects.values('id','name', 'division').distinct()
    #  class_list = [f"{item['name']} {item['division']}" for item in qs]
    #  print(class_list)
     course = Course.objects.all()
     examnames = ExamtypeSettings.objects.all()
     session = Session.objects.filter(is_active=True).first()
     context = {
          'courses': course,
          'examnames': examnames,
           'page_title': 'Result Bulk Upload',
           'session': session
     }
     
     return render(request, 'acc_admin_template/result_bulk_upload_template.html', context)

def result_page(request):
     form = upload_excel(request.POST, request.FILES)
     course = Course.objects.all()
     session = Session.objects.filter(is_active=True).first()
     context = {
          'courses': course,
           'page_title': 'Result Page',
           'session': session
     }
     
     return render(request, 'acc_admin_template/result_upload_template.html',context, )

def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES["excel_file"]

            try:
                df = pd.read_excel(excel_file)

                required_columns = {'test', 'subject_id', 'remarks', 'term', 'student_id', 'exam'}
                if not required_columns.issubset(df.columns):
                    missing_columns = required_columns - set(df.columns)
                    messages.error(request, f"Excel file is missing columns: {', '.join(missing_columns)}")
                    return redirect("upload_excel")

                records_saved = 0
                duplicate_entries = []
                subject_not_found = []

                for _, row in df.iterrows():
                    subject_name = str(row["subject_id"]).strip()
                    student_id = int(row["student_id"])
                    term = str(row["term"]).strip()

                    try:
                        subject_master = Subjectmaster.objects.get(name__iexact=subject_name)
                    except Subjectmaster.DoesNotExist:
                        subject_not_found.append(subject_name)
                        continue

                    try:
                        subject = Subject.objects.filter(subject=subject_master).first()
                        if not subject:
                            subject_not_found.append(subject_name + " (No linked Subject)")
                            continue

                    except Subject.DoesNotExist:
                        subject_not_found.append(subject_name + " (No linked Subject)")
                        continue

                    if StudentResult.objects.filter(
                        student_id=student_id,
                        subject=subject,
                        term=term
                    ).exists():
                        duplicate_entries.append(
                            f"Student ID {student_id} - Subject '{subject_name}' - Term {term}"
                        )
                        continue

                    StudentResult.objects.create(
                        test=str(row["test"]).strip(),
                        subject=subject,
                        subjectmaster=subject_master,
                        term=term,
                        remarks=str(row["remarks"]).strip(),
                        student_id=student_id,
                        exam=str(row["exam"]).strip()
                    )
                    records_saved += 1

                if records_saved > 0:
                    messages.success(request, f"{records_saved} record(s) uploaded successfully.")

                if duplicate_entries:
                    messages.error(
                        request,
                        "This student/students already exists in this term."
                    )

                if subject_not_found:
                    unique_subjects = sorted(set(subject_not_found))
                    messages.warning(
                        request,
                        "Subjects not found and skipped:<br>" + "<br>".join(unique_subjects)
                    )

                return redirect("upload_excel")

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect("upload_excel")

    else:
        form = ExcelUploadForm()

    return render(request, "acc_admin_template/upload_exel.html", {"form": form})


@csrf_exempt
def get_students_list(request):
      course = request.POST.get('course')
      subject_data1 = request.POST.get('subject_data1')
      try:
         course = get_object_or_404(Course, id=course)
         subject_data1 = get_object_or_404(Subjectmaster, id=subject_data1)
         students_with_subjects = Student.objects.filter(
    course_id=course,
    course_id__in=Subject.objects.filter(course_id=course, subject_id=subject_data1).values_list('course_id', flat=True)
)
         bulk_data = []
         for student in students_with_subjects:
           data = {
                       "id": student.id,
                        "name": student.admin.first_name + " " + student.admin.last_name,
                        "admission_number": student.admission_number
                  }
           bulk_data.append(data)
         return JsonResponse(json.dumps(bulk_data), content_type='application/json', safe=False)
      except Exception as e:
         return e  
    

def save_excel_data(request,course,subject_data1):
      # Set up the data for the form
   
    course_obj = get_object_or_404(Course, id=course)
    subject = get_object_or_404(Subjectmaster,id=subject_data1)
   
    students_with_subjects = Student.objects.filter(
    course_id=course_obj,
    course_id__in=Subject.objects.filter(course_id=course_obj, subject_id=subject).values_list('course_id', flat=True))
      # Set up the data for the form  
    
    data_bulk =[]
    for student in students_with_subjects:
      data = {
            #    "Admission Number":student.admission_number,
               "Student Name": student.admin.first_name + " " + student.admin.last_name,
               "student_id": student.id,
               "test": "",
               "exam": "",
               "remarks": "",
               "term": "Term-1",
               "subject_id": subject.name,
             }
      data_bulk.append(data)
      df = pd.DataFrame(data_bulk)

    # Create an Excel workbook and add a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Form"

    # Add data to the worksheet
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)

    # Style headers
    header_fill = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
    header_font = Font(bold=True, color="000000")
    for cell in ws["1:1"]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Adjust column widths
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 15
    ws.column_dimensions["F"].width = 15
    # ws.column_dimensions["G"].width = 15

    # Apply borders
    thin_border = Border(left=Side(style="thin"), right=Side(style="thin"),
                         top=Side(style="thin"), bottom=Side(style="thin"))
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=2):
        for cell in row:
            cell.border = thin_border

    # Save the workbook to a BytesIO object
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Create HTTP response for download
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Excel_Form_Template.xlsx"'

    return response

@csrf_exempt
def get_students_bulk(request):
      
        course = request.POST.get('course')
        subject_data_value1 = request.POST.get('subject_data_value1')
        session = request.POST.get('session')
            # print(subject_data_value1)
        try:
          course = get_object_or_404(Course, id=course)
        #   print(course)
          subject_data_value = get_object_or_404(Subject, id=subject_data_value1)
        #   print(subject_data_value)
#           students_with_subjects = Student.objects.filter(
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


        #   print(students_with_subjects)
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
         return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
def get_course_list(request):
    course_id = request.POST.get('course')
    subject_names = Subject.objects.filter(course_id=course_id)
    subject_data_value = []
    for subject_name in subject_names:
        data = {
                 "id": subject_name.id,
                 "name": subject_name.subject.name,
                 "staff": subject_name.staff.admin.first_name + " " + subject_name.staff.admin.last_name if subject_name.staff.admin else "Not Assigned"
                }
        subject_data_value.append(data) 
    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)
def student_excelform(request):
    context = {
        'page_title': 'Student Excel Form',
    }
    return render(request, 'acc_admin_template/student_excelform_template.html', context)

def student_excelform2(request):
    context = {
        'page_title': 'Student Excel Form 2',
    }
    return render(request, 'acc_admin_template/student_excelform2_template.html', context)

def student_excel_data(request):
    # Create a new workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Student Data"

    # Define the headers
    headers = ["Admission Number", "First Name", "Last Name","Gender", "Email", "Course","Division","Parent Name","Mother Tongue"]

    # Write headers to the first row
    for col, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = Font(bold=True)

    # Set column widths
    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 20

    # Create data validation for the Admission Number column (assuming it should be a number)
    admission_number_dv = DataValidation(type="whole", operator="greaterThan", formula1=0)
    admission_number_dv.error = 'Please enter a valid admission number'
    admission_number_dv.errorTitle = 'Invalid Admission Number'

    # Add the data validation to the Admission Number column
    sheet.add_data_validation(admission_number_dv)
    admission_number_dv.add(f'A2:A1048576')  # Apply to all rows in column A (Admission Number)

    # Create the HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_data_form.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response

def student_excel_data2(request):
    # Create a new workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Student Data Sheet"

    # Define the headers
    headers = ["First Name", "Last Name","Course","Division"]

    # Write headers to the first row
    for col, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col)
        cell.value = header
        cell.font = Font(bold=True)

    # Set column widths
    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 20
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_data_form.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response



def upload_student_data(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active

            for row in worksheet.iter_rows(min_row=2, values_only=True):

                try:
                    admission_number, first_name, last_name, gender, email, course_name, course_division, parent_name, mother_tongue = row

                    if not all([first_name, last_name, gender, email, course_name, course_division, parent_name, mother_tongue]):
                        print(f"Skipping row due to missing values: {row}")
                        continue
                    # Check if admission number is null
                    if not admission_number:
                        messages.error(request, "Admission number is missing. Skipping row.")
                        continue

                    # Check if admission number already exists
                    existing_student = Student.objects.filter(admission_number=admission_number).first()
                    if existing_student:
                        messages.error(request, f"Admission number {admission_number} already exists for {existing_student.admin.first_name} {existing_student.admin.last_name}.")
                        continue

                    user, user_created = CustomUser.objects.get_or_create(
                        email=email,
                        defaults={
                            "user_type": 3,
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender
                        }
                    )

                    if not user_created:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.gender = gender
                        # user.set_password(password)
                        user.save()

                    try:
                        course_instance = Course.objects.filter(name=course_name, division=course_division).first()
                        if not course_instance:
                            print(f"Course {course_name} - {course_division} not found, skipping row!")
                            continue
                    except Course.DoesNotExist:
                        print(f"Course {course_name} not found, skipping row!")
                        continue

                    student, student_created = Student.objects.update_or_create(
                        admin=user,
                        defaults={
                            "course": course_instance,
                            "session": None,
                            "admission_number": admission_number,
                            "parent_name": parent_name,
                            "mother_tongue": mother_tongue,
                            "gender": gender,
                            "file_type": "1",
                        }
                    )

                    if student_created:
                        print(f"New student created with admission number {admission_number}")
                    else:
                        print(f"Existing student updated for admission number {admission_number}")

                except Exception as e:
                    print("Unexpected Error:", str(e))

                messages.success(request, "Student data uploaded successfully!")
            return redirect('upload_student_data')

    else:
        form = ExcelUploadForm()

    return render(request, 'acc_admin_template/student_uploadform_template.html', {'form': form})

def upload_student_data2(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active

            user_counter = 1  # Unique ID starts here

            for row in worksheet.iter_rows(min_row=2, values_only=True):
                try:
                    first_name, last_name,gender, course_name, course_division = row

                    if not all([first_name, last_name,gender, course_name, course_division]):
                        print(f"Skipping row due to missing values: {row}")
                        continue

                    # Generate email using user_counter as the user_id
                    email = generate_unique_email(first_name, last_name, user_counter)
                    user_counter += 1  # Increment the counter for the next user

                    user, user_created = CustomUser.objects.get_or_create(
                        email=email,
                        defaults={
                            "user_type": 3,
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender
                        }
                    )

                    course_instance = Course.objects.filter(
                        name=course_name,
                        division=course_division
                    ).first()

                    if not course_instance:
                        print(f"Course {course_name} - {course_division} not found, skipping row!")
                        continue

                    student, student_created = Student.objects.update_or_create(
                        admin=user,
                        defaults={
                            "course": course_instance,
                            "session": None,
                            "file_type": "1",
                        }
                    )

                    if student_created:
                        print(f"New student created: {first_name} {last_name}")
                    else:
                        print(f"Existing student updated: {first_name} {last_name}")

                except Exception as e:
                    print("Unexpected Error:", str(e))

            messages.success(request, "Student data uploaded successfully!")
            return redirect('upload_student_data2')

    else:
        form = ExcelUploadForm()

    return render(request, 'acc_admin_template/student_uploadform2_template.html', {'form': form})


def generate_unique_email(first_name, last_name, user_id):
    email_local = f"{first_name.lower()}{last_name.lower()}{user_id}"
    return f"{email_local}@littleflower.school"



def academic_admin_view_profile(request):
    # Automatically create AccAdmin object if it doesn't exist
    if request.user.user_type == '4':  # 4 = Academic Admin
        accadmin_obj, created = AccAdmin.objects.get_or_create(accadmin=request.user)
    else:
        messages.error(request, "Unauthorized access.")
        return redirect('login')  # Or any appropriate fallback

    form = AccAdminForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST':
        try:
            if form.is_valid():
                updated_user = form.save(commit=False)
                new_password = form.cleaned_data.get('new_password')

                if new_password:
                    updated_user.set_password(new_password)

                updated_user.save()
                messages.success(request, "Profile updated successfully!")
                return redirect(reverse('academic_admin_view_profile'))
            else:
                messages.error(request, "Invalid data provided.")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")

    context = {
        'form': form,
        'page_title': 'View/Edit Profile'
    }
    return render(request, 'acc_admin_template/academic_admin_view_profile.html', context)


def send_notification(request, id):
    curriculam = get_object_or_404(Curriculam, id=id)
    
    if curriculam.notificaton == 'False':
        curriculam.notificaton = 'True'
        curriculam.save()
        messages.success(request, f"Notification sent for curriculum: {curriculam.lesson}")
    else:
        messages.info(request, f"Notification was already sent for curriculum: {curriculam.lesson}")
    
    return redirect('manage_curriculam')  # Assuming 'manage_curriculam' is the name of the URL for the curriculum list page

@csrf_exempt
@require_POST
def save_student_results(request):
    try:
        data = json.loads(request.body)
        created_count = 0
        updated_count = 0
        failed = []

        for entry in data:
            try:
                student_id = entry.get("student_id")
                subject_id = entry.get("subject_id")
                course_id = entry.get("course")
                session_id = entry.get("session_id")   # <-- IMPORTANT

                term = (entry.get("term") or "").strip()
                exam_type_code = (entry.get("exam_type") or "").strip()
                remarks = (entry.get("remarks") or "").strip()

                # Convert marks safely
                try:
                    test_score = float(entry.get("test") or 0)
                    exam_score = float(entry.get("exam") or 0)
                    semester_score = float(entry.get("semester") or 0)
                except (ValueError, TypeError):
                    failed.append(f"Invalid marks for Student {student_id}")
                    continue

                print("\n==============================")
                print(entry)

                # Required fields
                if not all([
                    student_id,
                    subject_id,
                    course_id,
                    session_id,
                    term,
                    exam_type_code
                ]):
                    failed.append(f"Missing required fields : {entry}")
                    continue

                # Skip blank row
                if (
                    test_score == 0 and
                    exam_score == 0 and
                    semester_score == 0 and
                    not remarks
                ):
                    continue

                # Only one mark allowed
                score_count = sum([
                    test_score > 0,
                    exam_score > 0,
                    semester_score > 0,
                ])

                if score_count > 1:
                    failed.append(
                        f"Student {student_id}: Only one mark field is allowed."
                    )
                    continue

                if score_count == 0 and not remarks:
                    remarks = "Absent"

                # Student
                try:
                    student = Student.objects.get(pk=student_id)
                except Student.DoesNotExist:
                    failed.append(f"Student {student_id} not found.")
                    continue

                # Subject
                try:
                    subject = Subject.objects.get(
                        pk=subject_id,
                        course_id=course_id
                    )
                except Subject.DoesNotExist:
                    failed.append(f"Subject {subject_id} not found.")
                    continue

                # Session
                try:
                    session = Session.objects.get(pk=session_id)
                except Session.DoesNotExist:
                    failed.append(f"Session {session_id} not found.")
                    continue

                # Exam Type
                try:
                    exam = ExamtypeSettings.objects.get(
                        exam_name__iexact=exam_type_code
                    )
                except ExamtypeSettings.DoesNotExist:
                    failed.append(
                        f"Exam Type '{exam_type_code}' not found."
                    )
                    continue

                # Subject Master
                subjectmaster = subject.subject

                with transaction.atomic():

                    result, created = StudentResult.objects.update_or_create(
                        student=student,
                        subject=subject,
                        exam_type=exam,
                        session=session,
                        term=term,
                        defaults={
                            "subjectmaster": subjectmaster,
                            "test": str(test_score),
                            "exam": str(exam_score),
                            "semester": str(semester_score),
                            "remarks": remarks,
                        },
                    )

                if created:
                    created_count += 1
                    print(f"Created -> {student}")
                else:
                    updated_count += 1
                    print(f"Updated -> {student}")

            except Exception as e:
                print(traceback.format_exc())
                failed.append(
                    f"Student {entry.get('student_id')} : {str(e)}"
                )

        total = created_count + updated_count

        if total == 0:
            return JsonResponse({
                "status": "empty",
                "message": "No records saved.",
                "created": created_count,
                "updated": updated_count,
                "failures": failed
            })

        return JsonResponse({
            "status": "success",
            "message": f"{created_count} created, {updated_count} updated.",
            "created": created_count,
            "updated": updated_count,
            "failures": failed
        })

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
@csrf_exempt
def manage_curriculam_data(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        subject_data = request.POST.get('subject_data')
        term_wise = request.POST.get('term_wise')
        curriculams = Curriculam.objects.filter(course_id=course_id, subject_id=subject_data, term=term_wise)
        curriculam_data = []

        for curriculam in curriculams:
            curriculam_data.append({
                "id": curriculam.id,
                "lesson": curriculam.lesson,
                "course": curriculam.course.name,
                 "division": curriculam.course.division,
                 "subject": curriculam.subject.subject.name,
                "term": curriculam.term,
                "status":curriculam.status,
                "notificaton": curriculam.notificaton,
            })
        return JsonResponse(curriculam_data, safe=False)  # No need for json.dumps

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def view_filtered_class_results(request):
    courses = Course.objects.all()
    session = Session.objects.filter(is_active=True).first()
    terms = ExamtypeSettings.objects.values_list('term', flat=True).distinct()

    selected_course = ""
    selected_term = ""
    selected_exam = ""
    selected_exam_name = ""

    student_data = defaultdict(lambda: {
        "marks": {},
        "percentage": 0,
        "name": ""
    })

    all_subjects = set()
    results = []
    exams = []

    if request.GET.get("course") and request.GET.get("term") and request.GET.get("exam"):

        selected_course = request.GET.get("course")
        selected_term = request.GET.get("term")
        selected_exam = request.GET.get("exam")
        session_id = request.GET.get("session_select")

        exams = ExamtypeSettings.objects.filter(term=selected_term)

        try:
            exam_obj = ExamtypeSettings.objects.get(id=selected_exam)
            selected_exam_name = exam_obj.exam_name
            max_marks = exam_obj.max_marks
        except ExamtypeSettings.DoesNotExist:
            selected_exam_name = ""
            max_marks = 20

        students = Student.objects.filter(course_id=selected_course)

        results = StudentResult.objects.filter(
            student__in=students,
            exam_type_id=selected_exam,
            session_id=session_id,
            term=selected_term
        ).select_related(
            "student__admin",
            "subject__subject",
            "exam_type"
        )

        print("Results Count :", results.count())

        for row in results:

            print(
                row.student.id,
                row.subject.subject.name,
                row.test,
                row.exam,
                row.semester
            )

            student_name = f"{row.student.admin.first_name} {row.student.admin.last_name}"

            subject_name = row.subject.subject.name
            all_subjects.add(subject_name)

            exam_name = selected_exam_name.upper()

            if "PT" in exam_name:
                mark = row.test
            elif "TP" in exam_name:
                mark = row.exam
            elif "SEMESTER" in exam_name:
                mark = row.semester
            else:
                mark = row.test

            student_data[row.student.id]["name"] = student_name
            student_data[row.student.id]["marks"][subject_name] = mark

        for student in student_data.values():

            total = 0
            total_max = 0

            for mark in student["marks"].values():

                try:
                    total += float(mark)
                    total_max += float(max_marks)
                except:
                    pass

            if total_max:
                student["percentage"] = round((total / total_max) * 100, 2)

    else:
        exams = []

    context = {
        "courses": courses,
        "terms": terms,
        "exams": exams,
        "student_subject_marks": student_data.values(),
        "subjects": sorted(all_subjects),
        "selected_course": selected_course,
        "selected_term": selected_term,
        "selected_exam": selected_exam,
        "selected_exam_name": selected_exam_name,
        "results": results,
        "session": session,
        "page_title": "Class Wise Result",
    }

    return render(
        request,
        "acc_admin_template/class_wise_result.html",
        context
    )
@csrf_exempt  # If you're not using csrf_token properly
def get_exams_by_term(request):
    if request.method == "POST":
        term = request.POST.get("term")
        exams_qs = ExamtypeSettings.objects.filter(term=term).values("id", "exam_name")
        
        exams = list(exams_qs)  # Convert queryset to list of dicts

        return JsonResponse(exams, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)

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
    return render(request, "acc_admin_template/class_wise_result_subject.html", context)

def add_examtype_settings(request):
    form = ExamtypeSettingsForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            exam_type = form.cleaned_data.get('exam_type')
            exam_name = form.cleaned_data.get('exam_name')
            term = form.cleaned_data.get('term')
            max_marks = form.cleaned_data.get('max_marks')
            exam_date = form.cleaned_data.get('exam_date')
            if ExamtypeSettings.objects.filter(exam_type=exam_type, exam_name=exam_name, term=term).exists():
                messages.warning(request, f"{exam_type} for {term} with name '{exam_name}' already exists.")
            else:
                # Create the ExamtypeSettings instance
                ExamtypeSettings.objects.create(
                    exam_type=exam_type,
                    exam_name=exam_name,
                    term=term,
                    max_marks=max_marks,
                    exam_date=exam_date
            )

            # Optional: Prevent duplicate entry
           
            # else:
            #     form.save()
                messages.success(request, "Exam type settings added successfully.")
                return redirect('add_examtype_settings')  # Replace with your URL name

    context = {
        'form': form,
        'page_title': "Add Exam Type Settings",
    }
    return render(request, "acc_admin_template/add_examsetting_template.html", context)

def manage_examtype_settings(request):
    examsettings = ExamtypeSettings.objects.all()
    context = {
          'examsettings': examsettings,
          'page_title': 'Manage Exam Type Settings'
     }
    return render(request, 'acc_admin_template/manage_examsetting_template.html',context)

def edit_examtype_settings(request, id):
    examtype = get_object_or_404(ExamtypeSettings, id=id)
    form = ExamtypeSettingsForm(request.POST or None, instance=examtype)

    context = {
        'form': form,
        'page_title': 'Edit Exam Type Settings',
        'id': id,
        'examtype': examtype,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('manage_examtype_settings'))  # Change to your actual manage URL name
        else:
            messages.error(request, "Please correct the errors below.")
    
    return render(request, 'acc_admin_template/edit_examsetting_template.html', context)

def delete_examtype_settings(request, id):
    examtype = get_object_or_404(ExamtypeSettings, id=id)
    examtype.delete()
    messages.success(request, "Successfully Deleted")
    return redirect(reverse('manage_examtype_settings'))  # Change to your actual manage URL name
def get_term_list(request):
    exam_name = request.POST.get('exam_name')
    examtype = ExamtypeSettings.objects.get(id=exam_name)
    term_list = examtype.term.split(",")  # Assuming CSV string
    term_select = [{'id': i + 1, 'name': term.strip()} for i, term in enumerate(term_list)]
    return JsonResponse(term_select, safe=False)

def manage_bulk_result(request):

    course = Course.objects.all()
    examnames = ExamtypeSettings.objects.all()
    sessions = Session.objects.filter(
        is_active=True
    ).first()
    context = {
         'courses': course,
          'examnames': examnames,
        'page_title': 'Manage Bulk Result',
        'session': sessions
    }
    return render(request, 'acc_admin_template/manage_bulk_result.html', context)
def bulk_student_data(request):
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
    session=session_obj
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
                "exam": r.exam,
                "remarks": r.remarks,
                "semester": r.semester,

}
                bulk_data_list.append(data)

        return JsonResponse(bulk_data_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def edit_bulkresult(request, result_id):
    instance = get_object_or_404(StudentResult, id=result_id)

    # Get max_marks from ExamtypeSettings
    exam_setting = ExamtypeSettings.objects.filter(
        exam_name=instance.exam_type.exam_name,
        # exam_type=instance.exam_type,
        term=instance.term
    ).first()
    session =Session.objects.filter(is_active=True).first()
    
    max_marks = exam_setting.max_marks if exam_setting else 20

    context = {
        'page_title': 'Edit BulkResult',
        'result': instance,
        'max_marks': max_marks,
        'courses': Course.objects.all(),
        'subjects': Subject.objects.all(),
        'examnames': ExamtypeSettings.objects.all(),
        'session': session
    }
   

    return render(request, 'acc_admin_template/edit_bulk_result.html',context)

def delete_bulkresult(request,result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    
    # Clear only the marks (fields might differ based on your model)
    result.test = 0
    result.exam = 0
    result.semester = 0
    result.remarks = ""
    result.save()

    messages.success(request, "Result marks cleared successfully.")
    return redirect('manage_bulk_result')

EXAM_COLUMNS = [
    'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7', 'TP8', 'TP9', 'TP10', 'TP11', 'TP12',
    'PT1', 'PT2', 'PT3',
    'SEMESTER1', 'SEMESTER2'
]


def new_class_result(request):
    courses = Course.objects.all()
    session = Session.objects.filter(is_active=True).first()
    subjects = Subject.objects.none()
    selected_course = request.GET.get('course')
    selected_subject = request.GET.get('subject')
    session_id =request.GET.get('session_select') or session.id if session else None
    all_data = []
    exam_columns = []
    staff_name = "Not Assigned"  # default

    if selected_course:
        subjects = Subject.objects.filter(course_id=selected_course)

        # ✅ Pick first subject's staff if available
        if subjects.exists():
            first_subject = subjects.first()
            if first_subject.staff and first_subject.staff.admin:
                staff_name = f"{first_subject.staff.admin.first_name} {first_subject.staff.admin.last_name}"

        if selected_subject:
            selected_subject = int(selected_subject)
            students = Student.objects.filter(course_id=selected_course)

            # ✅ Fetch dynamic exam names
            exam_columns_qs = ExamtypeSettings.objects.all().order_by('id')
            exam_columns = [e.exam_name.strip().upper() for e in exam_columns_qs]

            results_qs = StudentResult.objects.filter(
                student__in=students,
                subject__id=selected_subject,
                session_id=session_id
            ).select_related('student__admin', 'exam_type')

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
        'session': session,
        'page_title': "Subjectwise Result",
        'staff': staff_name,  # ✅ fixed
    }

    return render(request, 'acc_admin_template/classwise_result.html', context)

def update_student_bulk_result(request, result_id):
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
            return redirect('manage_bulk_result')  # Change this to your actual result listing page

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
     return render(request, "acc_admin_template/edit_bulk_result.html", context)

def acc_admin_studentgraph(request):
    courses = Course.objects.all() 
    session = Session.objects.filter(is_active=True).first()
    context ={
        "page_title":"Student Graphwise",
         "courses":courses,
         "session": session
    }
    return render(request, "acc_admin_template/acadmin_studentgraph.html", context)

def acc_admin_studentexamwisegraph(request):
    courses = Course.objects.all()
    exams= ExamtypeSettings.objects.all()
    session = Session.objects.filter(is_active=True).first()
    context = {
       "page_title": "Student Exam Wise Graph",
       "exams": exams,
       "courses": courses,
       "session": session
   }
    return render(request, "acc_admin_template/acc_admin_studentexamwisegraph.html",context)
def get_student_bargraph(request):
    student_id = request.GET.get('student_id')
    exam_id = request.GET.get('subject_id') 
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
            "marks": marks,
            
        })
       
    return JsonResponse({
        'data': subject_marks,
        'max_mark': max_mark
    })

def get_subject(request):
    course_id = request.POST.get('course')
    subject_names = Subject.objects.filter(course_id=course_id)
    subject_data_value = []
    for subject_name in subject_names:
        data = {
                 "id": subject_name.id,
                 "name": subject_name.subject.name 
                }
        
        subject_data_value.append(data) 
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

def marks_graph_page(request):
    return render(request, 'acc_admin_template/acadmin_studentgraph.html')

# def get_student_marks(request):
   
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
#             return (1, int(name[2:]))
#         elif name.startswith('PT'):
#             return (2, int(name[2:]))
#         elif 'SEMESTER' in name:
#             return (3, int(name.replace('SEMESTER', '').strip() or 0))
#         return (4, 0)

#     results = sorted(results, key=sort_key)

#     data = []
#     data_list = []


#     for result in results:
#         exam_name = result.exam_type.exam_name.strip()
#         exam_type = result.exam_type.exam_type.strip().lower()  # You should have this field
#         raw = result.test or result.exam or result.semester  # fallback logic

#         if raw not in [None, '']:
#             try:
#                 marks = float(raw)
#                 data.append({
#                     "exam_name": exam_name,
#                     "exam_type": exam_type,  # like 'test paper', 'periodic test', 'semester'
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
def  acc_admin_staffgraph(request):
    courses = Course.objects.all()
    staff= Staff.objects.all()
    session = Session.objects.filter(is_active=True).first()
    exam_type = ExamtypeSettings.objects.all()
    context = {
        "page_title": "Exam-wise Staff Performance",
        "courses": courses,
        "staff_members":staff,
        "exam_type": exam_type,
        "session": session
    }
    return render(request, "acc_admin_template/staffgraph.html",context)
def get_staff(request):
    course_id = request.POST.get('course')
    subject_id = request.POST.get('subject')
   
    staff_data = []

    try:
        course = get_object_or_404(Course, id=course_id)
        staff_members = Subject.objects.filter(course_id=course_id , subject_id=subject_id)
        # print("Staff members found:", staff_members)
        for subject in staff_members:
            staff = subject.staff
            # print(subject.staff.first_name, subject.staff.last_name)  # ForeignKey from Subject to Staff
            staff_data.append({
                "id": subject.staff_id,
                "name": f"{subject.staff} "  # adjust based on your model
            })
        # print("Staff data prepared:", staff_data)
        return JsonResponse(staff_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# or MainAppSubject if needed

def get_subject_staff(request):  
    course_id = request.POST.get('course')
    # print("Received course ID111:", course_id)

    subject_names = Subject.objects.filter(course_id=course_id)
    subject_data_value = []
    # print("Subject names founddddd:", subject_names)
    for subject_name in subject_names:
        data = {
            "id": subject_name.subject_id,
            "name": subject_name.subject.name  # Assuming 'subject' is a ForeignKey
        }
      
        subject_data_value.append(data)

    return JsonResponse(subject_data_value, safe=False)

def get_staff_graph(request):
    staff_id = request.GET.get('staff_id')
    exam_id = request.GET.get('exam_id')
    session_id = request.GET.get('session_id')

    subject_qs = Subject.objects.filter(staff_id=staff_id)
    if not subject_qs.exists():
        return JsonResponse({"error": "No subjects found for this staff"}, status=404)

    subject_ids = subject_qs.values_list('id', flat=True)

    results = StudentResult.objects.filter(
        subject_id__in=subject_ids,
        exam_type_id=exam_id,
        session_id=session_id
    ).select_related('student__course', 'subject', 'subject__course', 'exam_type')

    if not results.exists():
        return JsonResponse({"error": "No results found"}, status=404)

    # Get max_marks from exam type table
    exam_type_obj = ExamtypeSettings.objects.filter(id=exam_id).first()
    try:
        max_marks = float(exam_type_obj.max_marks) if exam_type_obj and exam_type_obj.max_marks else 0.0
    except ValueError:
        max_marks = 0.0

    grouped = defaultdict(list)
    for res in results:
        course_name = res.subject.course.name + "-" + res.subject.course.division
        key = (course_name, res.subject.subject.name)
        grouped[key].append(res)

    subjects_data = []
    percentage_color_map = {}  # 🎯 Store colors for each unique percentage

    def get_color_for_percentage(percentage):
        """Return same color for same percentage"""
        if percentage in percentage_color_map:
            return percentage_color_map[percentage]

        # Assign new color
        
        if percentage >= 75:
            color = "#146b0cff"
        elif percentage >= 60:
            color = "#28e141ff"
        elif percentage >= 50:
            color = "#ffc107"
        elif percentage >= 35:
            color = "#e3d10cff"
        # elif percentage >= 50:
        #     color = "#e0731aff"
        else:
            color = "#f6061eff"

        percentage_color_map[percentage] = color
        return color

    for (course_name, subject_name), res_list in grouped.items():
        student_ids = set(r.student_id for r in res_list)

        student_graph_data = []
        for stu_id in student_ids:
            student_obj = Student.objects.select_related('course', 'admin').get(id=stu_id)
            stu_results = [r for r in res_list if r.student_id == stu_id]

            marks_dict = {}
            for r in stu_results:
                try:
                    mark_obtained = float(r.test) if r.test is not None else 0.0
                except ValueError:
                    mark_obtained = 0.0

                percentage = round((mark_obtained / max_marks) * 100, 2) if max_marks else 0
                color = get_color_for_percentage(percentage)  # 🎯 Use consistent color

                marks_dict[r.exam_type.exam_name] = {
                    "percentage": percentage,
                    "color": color
                }

            student_graph_data.append({
                "student_name": student_obj.admin.first_name,
                "marks": marks_dict
            })

        labels = sorted(set(r.exam_type.exam_name for r in res_list))

        subjects_data.append({
            "course_name": course_name,
            "subject_name": subject_name,
            "labels": labels,
            "students": student_graph_data
        })
    return JsonResponse({"subjects": subjects_data})


def getmaxmarks(request):
    exam_id = request.GET.get('exam_id')
  

    try:
        exam = ExamtypeSettings.objects.get(id=exam_id)
        # print(f"Max marks found: {exam.max_marks}")
        return JsonResponse({'max_marks': exam.max_marks})
    except ExamtypeSettings.DoesNotExist:
        # print("Exam not found.")
        return JsonResponse({'error': 'Invalid Exam ID'}, status=400)
    
def get_subjects(request):
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
            "name": subject.subject.name,
            "staff": str(subject.staff) if subject.staff else "Not Assigned"
        })
    # print(subject_data_value)
    return JsonResponse(json.dumps(subject_data_value), content_type='application/json', safe=False)

@csrf_exempt
def get_students(request):
    course_id = request.POST.get('course')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    # print(course_id, subject_id, session_id)
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


# @csrf_exempt
@require_GET
@login_required  # remove this if you want it public
def examtypecolors(request):
    exam_types = ExamtypeSettings.objects.values('exam_type', 'exam_name').distinct()
    data = {item['exam_type'].lower(): item['exam_name'] for item in exam_types}

    return JsonResponse(data)
def admin_studentexamgraph(request):
   courses = Course.objects.all()
   exams= ExamtypeSettings.objects.all()
   context = {
       "page_title": "Student Exam Wise Graph",
       "exams": exams,
       "courses": courses,
   }
   return render(request, "acc_admin_template/admin_studentexamgraph.html", context)      
def academic_admin_studentexamgraph(request):
   courses = Course.objects.all()
   exams= ExamtypeSettings.objects.all()
   context = {
       "page_title": "Student Exam Wise Graph",
       "exams": exams,
       "courses": courses,
   }
   return render(request, "acc_admin_template/academicadmin_studentexamgraph.html", context) 
def acc_admin_staffgraph2(request) :
    courses = Course.objects.all()
    exam_type = ExamtypeSettings.objects.all()
    session = Session.objects.filter(is_active=True).first()
    context = {
        "page_title": "Student-wise Staff Performance",
        "courses": courses,
        "exam_type": exam_type,
        "session": session
    }
    return render(request, "acc_admin_template/staffgraph2.html",context)

def get_student_pie_data(request):
    course_id = request.GET.get('course')
    subject_id = request.GET.get('subject')
    staff_id = request.GET.get('staff')
    exam_id = request.GET.get('exam')
    session_id = request.GET.get('session')
    print("Received parameters:", course_id, subject_id, staff_id, exam_id, session_id)
    # Validate exam ID
    try:
        exam_id = int(float(exam_id)) if exam_id else None
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid exam ID'}, status=400)

    # Fetch subject
    subject = Subject.objects.filter(
        course_id=course_id,
        subject_id=subject_id,
        staff_id=staff_id,
    ).first()

    if not subject:
        return JsonResponse({'error': 'Subject not found'}, status=404)

    # Fetch exam type only once
    exam_type = ExamtypeSettings.objects.filter(id=exam_id).first()
    if not exam_type or exam_type.max_marks == 0:
        return JsonResponse({'error': 'Invalid exam type or max marks'}, status=400)

    # Fetch results with related Student & Admin in one query
    results = (
        StudentResult.objects
        .filter(subject_id=subject.id, exam_type_id=exam_id, session_id=session_id)
        .select_related('student__admin')
    )

    labels = []
    percentages = []
    background_colors = []

    for result in results:
        try:
            mark = float(result.test)
        except (ValueError, TypeError):
            continue

        percentage = (mark / exam_type.max_marks) * 100
        full_name = f"{result.student.admin.first_name} {result.student.admin.last_name}"

        labels.append(full_name)
        percentages.append(round(percentage, 2))

        # Color selection
        if percentage >= 75:
            color = "#146b0cff"
        elif percentage >= 60:
            color = "#28e141ff"
        elif percentage >= 50:
            color = "#ffc107"
        elif percentage >= 35:
            color = "#e3d10cff"
        # elif percentage >= 50:
        #     color = "#e0731aff"
        else:
            color = "#f6061eff"

        background_colors.append(color)

    return JsonResponse({
        'labels': labels,
        'percentages': percentages,
        'colors': background_colors
    })
def classwise_examreport(request):
    courses = Course.objects.all()
    staff = Staff.objects.all()
    session = Session.objects.filter(is_active=True).first()
    exam_type = ExamtypeSettings.objects.all()
    context = {
        "page_title": "Class wise Examination Mark Report",
        "courses": courses,
        "staff_members": staff,
        "session": session,
        "exam_type": exam_type
    }
    return render(request, "acc_admin_template/classwise_examreport.html", context)
def get_staff_graphmark(request):
    staff_id = request.GET.get('staff_id')
    exam_id = request.GET.get('exam_id')
    session_id = request.GET.get('session_id')

    subject_qs = Subject.objects.filter(staff_id=staff_id)
    if not subject_qs.exists():
        return JsonResponse({"error": "No subjects found for this staff"}, status=404)

    subject_ids = subject_qs.values_list('id', flat=True)

    results = StudentResult.objects.filter(
        subject_id__in=subject_ids,
        exam_type_id=exam_id,
        session_id=session_id
    ).select_related('student__course', 'subject', 'subject__course', 'exam_type')

    if not results.exists():
        return JsonResponse({"error": "No results found"}, status=404)

    exam_type_obj = ExamtypeSettings.objects.filter(id=exam_id).first()
    try:
        max_marks = float(exam_type_obj.max_marks) if exam_type_obj and exam_type_obj.max_marks else 0.0
    except ValueError:
        max_marks = 0.0

    grouped = defaultdict(list)
    for res in results:
        course_name = res.subject.course.name + "-" + res.subject.course.division
        key = (course_name, res.subject.subject.name)
        grouped[key].append(res)

    subjects_data = []

    for (course_name, subject_name), res_list in grouped.items():
        student_ids = set(r.student_id for r in res_list)

        student_graph_data = []
        for stu_id in student_ids:
            student_obj = Student.objects.select_related('course', 'admin').get(id=stu_id)
            stu_results = [r for r in res_list if r.student_id == stu_id]

            marks_dict = {}
            for r in stu_results:
                try:
                    mark_obtained = float(r.test) if r.test is not None else 0.0
                except ValueError:
                    mark_obtained = 0.0

                percentage = round((mark_obtained / max_marks) * 100, 2) if max_marks else 0
                marks_dict[r.exam_type.exam_name] = {
                    "percentage": percentage,
                }

            student_graph_data.append({
                "student_name": student_obj.admin.first_name,
                "marks": marks_dict
            })
            for r in stu_results:
             try:
               mark_obtained = float(r.test) if r.test is not None else 0.0
             except ValueError:
               mark_obtained = 0.0

             percentage = round((mark_obtained / max_marks) * 100, 2) if max_marks else 0
             marks_dict[r.exam_type.exam_name] = {
             "mark": mark_obtained,
             "percentage": percentage,
    }

        labels = sorted(set(r.exam_type.exam_name for r in res_list))

        subjects_data.append({
            "course_name": course_name,
            "subject_name": subject_name,
            "labels": labels,
            "students": student_graph_data
        })

    return JsonResponse({
        "subjects": subjects_data,
        "exam_name": exam_type_obj.exam_name if exam_type_obj else ""
    })

def teachers_list(request):
    teachers = Staff.objects.all()
    context = {
        "page_title": "Authorized Teachers",
        "teachers": teachers
    }
    return render(request, "acc_admin_template/teachers_list.html", context)
def update_permission(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_teachers')

        if selected_ids:
            # Step 1: Enable permission for selected teachers
            Staff.objects.filter(id__in=selected_ids).update(permission=1)

            # Step 2: Deny permission for others
            Staff.objects.exclude(id__in=selected_ids).update(permission=0)

            messages.warning(request, "Permission denied  successfully!")
        else:
            # No teachers selected — deny all
            Staff.objects.update(permission=0)
            messages.success(request, "Permission enabled successfully!")

        return redirect('teachers_list')
    
def acc_admin_averagemark(request):
    courses = Course.objects.all()
    staff = Staff.objects.all()
    session = Session.objects.filter(is_active=True).first()
    exam_type = ExamtypeSettings.objects.all()
    context = {
        "page_title": "Average Mark Report",
        "courses": courses,
        "exam_type": exam_type,
        "staff_members": staff,
        "session": session
    }
    return render(request, "acc_admin_template/averagemark.html",context)
# def get_staff_average(request):
#     staff_id = request.GET.get('staff_id')

#     if not staff_id:
#         return JsonResponse({"error": "Missing staff ID"}, status=400)

#     subject_qs = Subject.objects.filter(staff_id=staff_id)
#     if not subject_qs.exists():
#         return JsonResponse({"error": "No subjects found for this staff"}, status=404)

#     subject_ids = subject_qs.values_list('id', flat=True)

#     results = StudentResult.objects.filter(
#         subject_id__in=subject_ids
#     ).select_related('student__course', 'subject__course', 'exam_type')
#     print(results)
#     if not results.exists():
#         return JsonResponse({"error": "No results found"}, status=404)

#     # ✅ Group by class and exam type
#     class_exam_data = defaultdict(lambda: defaultdict(list))

#     for res in results:
#         if not res.exam_type:
#             continue
#         course_name = f"{res.subject.course.name}-{res.subject.course.division}"
#         exam_name = res.exam_type.exam_name

#         try:
#             mark_obtained = float(res.test) if res.test is not None else 0.0
#             print("mark_obtained", mark_obtained)
#         except ValueError:
#             mark_obtained = 0.0

#         class_exam_data[course_name][exam_name].append(mark_obtained)

#     # ✅ Prepare average marks per exam per class
#     subjects_data = []
#     for course_name, exam_dict in class_exam_data.items():
#         labels = sorted(exam_dict.keys())
#         averages = [
#             round(sum(values) / len(values), 2) if values else 0
#             for values in [exam_dict[exam] for exam in labels]
#         ]

#         subjects_data.append({
#             "course_name": course_name,
#             "labels": labels,
#             "averages": averages,
#         })

#     return JsonResponse({"subjects": subjects_data})
def get_staff_average(request):
    staff_id = request.GET.get('staff_id')
    session_id = request.GET.get('session_id')

    if not staff_id:
        return JsonResponse({"error": "Missing staff ID"}, status=400)

    if not session_id:
        return JsonResponse({"error": "Missing session ID"}, status=400)

    # ✅ Find all subjects taught by this staff
    subject_qs = Subject.objects.filter(staff_id=staff_id).select_related('course', 'subject')
    if not subject_qs.exists():
        return JsonResponse({"error": "No subjects found for this staff"}, status=404)

    subject_ids = subject_qs.values_list('id', flat=True)

    # ✅ Fetch all results for those subjects
    results = StudentResult.objects.filter(
        subject_id__in=subject_ids,
        session_id=session_id
    ).select_related('student__course', 'subject__course', 'exam_type', 'subject__subject')

    if not results.exists():
        return JsonResponse({"error": "No results found"}, status=404)

    # ✅ Group by class and exam type
    class_exam_data = defaultdict(lambda: defaultdict(list))
    class_subjects = defaultdict(set)  # 👈 keep track of subjects per class

    for res in results:
        if not res.exam_type:
            continue

        course_name = f"{res.subject.course.name}-{res.subject.course.division}"
        exam_name = res.exam_type.exam_name

        # track subject
        class_subjects[course_name].add(res.subject.subject.name)

        max_marks = float(res.exam_type.max_marks) if res.exam_type.max_marks else 0
        try:
            mark_obtained = float(res.test) if res.test is not None else 0.0
        except ValueError:
            mark_obtained = 0.0

        percentage = round((mark_obtained / max_marks) * 100, 2) if max_marks else 0
        class_exam_data[course_name][exam_name].append(percentage)

    # ✅ Prepare graph data per class
    subjects_data = []
    for course_name, exam_dict in class_exam_data.items():
        labels = sorted(exam_dict.keys())
        averages = [
            round(sum(values) / len(values), 2) if values else 0
            for values in [exam_dict[exam] for exam in labels]
        ]

        subjects_data.append({
            "course_name": course_name,
            "subjects": sorted(list(class_subjects[course_name])),  # 👈 Added subjects per class
            "labels": labels,
            "averages": averages,
        })

    return JsonResponse({"subjects": subjects_data})


def acc_admin_student_promotion(request):
    """Student Promotion page for Academic Admin - allows promoting students to the next class/session."""
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {
        'page_title': 'Student Promotion',
        'courses': courses,
        'sessions': sessions,
    }
    return render(request, 'acc_admin_template/student_promotion.html', context)


def acc_admin_promotion_history(request):
    """Promotion History page for Academic Admin - grouped by Session and Class."""
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
            
            # Convert values to list
            batch_list = list(batches.values())
            batch_list.sort(key=lambda x: x['from_course'].name, reverse=True)
            
            history.append({
                'session': session,
                'batches': batch_list
            })

    context = {
        'page_title': 'Promotion History',
        'history': history,  # Changed from 'promotions' to 'history'
    }
    return render(request, 'acc_admin_template/promotion_history.html', context)


@csrf_exempt
def acc_admin_get_promotion_students(request):
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
def acc_admin_promote_students(request):
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


def acc_admin_promotion_detail(request, pk):
    """View to show old data of a promoted student for Academic Admin."""
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
    return render(request, 'acc_admin_template/promotion_detail.html', context)


def acc_admin_undo_promotion(request, promotion_id):
    """Reverts a student promotion for Academic Admin."""
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
        
    return redirect('acc_admin_promotion_history')




def acc_admin_export_promotion_pdf(request, from_session_id, to_session_id, from_course_id, to_course_id):
    """Exports promotion list to PDF for Academic Admin."""
    promotions = StudentPromotion.objects.filter(
        from_session_id=from_session_id,
        to_session_id=to_session_id,
        from_course_id=from_course_id,
        to_course_id=to_course_id
    ).select_related('student', 'student__admin', 'from_course', 'to_course', 'from_session', 'to_session')

    if not promotions.exists():
        messages.error(request, "No promotions found to export.")
        return redirect('acc_admin_promotion_history')

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



# ===================== LMS Views (AccAdmin - View Only) =====================

@login_required
def acc_admin_lms_dashboard(request):
    video_count = LMSVideo.objects.count()
    image_count = LMSImage.objects.count()
    note_count = LMSNote.objects.count()
    
    recent_videos = LMSVideo.objects.order_by('-created_at')[:5]
    recent_images = LMSImage.objects.order_by('-created_at')[:5]
    recent_notes = LMSNote.objects.order_by('-created_at')[:5]
    
    context = {
        'page_title': 'LMS Dashboard',
        'video_count': video_count,
        'image_count': image_count,
        'note_count': note_count,
        'recent_videos': recent_videos,
        'recent_images': recent_images,
        'recent_notes': recent_notes,
    }
    return render(request, "acc_admin_template/acc_admin_lms_dashboard.html", context)


@login_required
def acc_admin_view_lms_videos(request):
    videos = LMSVideo.objects.all().order_by('-created_at')
    course_id = request.GET.get('course')
    subject_id = request.GET.get('subject')

    if course_id:
        videos = videos.filter(course_id=course_id)
    if subject_id:
        videos = videos.filter(subject__subject_id=subject_id)

    context = {
        'page_title': 'View Videos',
        'videos': videos,
        'courses': Course.objects.all(),
        'selected_course': int(course_id) if course_id else None,
        'selected_subject': int(subject_id) if subject_id else None,
    }
    return render(request, "acc_admin_template/acc_admin_view_lms_videos.html", context)

@login_required
def acc_admin_view_lms_images(request):
    images = LMSImage.objects.all().order_by('-created_at')
    course_id = request.GET.get('course')
    subject_id = request.GET.get('subject')

    if course_id:
        images = images.filter(course_id=course_id)
    if subject_id:
        images = images.filter(subject__subject_id=subject_id)

    context = {
        'page_title': 'View Images',
        'images': images,
        'courses': Course.objects.all(),
        'selected_course': int(course_id) if course_id else None,
        'selected_subject': int(subject_id) if subject_id else None,
    }
    return render(request, "acc_admin_template/acc_admin_view_lms_images.html", context)

@login_required
def acc_admin_view_lms_notes(request):
    notes = LMSNote.objects.all().order_by('-created_at')
    course_id = request.GET.get('course')
    subject_id = request.GET.get('subject')

    if course_id:
        notes = notes.filter(course_id=course_id)
    if subject_id:
        notes = notes.filter(subject__subject_id=subject_id)

    context = {
        'page_title': 'View Notes',
        'notes': notes,
        'courses': Course.objects.all(),
        'selected_course': int(course_id) if course_id else None,
        'selected_subject': int(subject_id) if subject_id else None,
    }
    return render(request, "acc_admin_template/acc_admin_view_lms_notes.html", context)

def staff_performance(request):
    course = Course.objects.all() 
    exam = ExamtypeSettings.objects.all()
    session = Session.objects.filter(is_active=True).first()
    
    context = {
        "page_title": "Staff Performance (class-wise)",
        "course": course,
        "exam": exam,
        "session": session
        
    }
    return render(request, "acc_admin_template/staffperformance.html",context)
def subject_performance(request):
    context = {
        "subjects" :Subjectmaster.objects.all(),
        "exams" :ExamtypeSettings.objects.all(),
        "session" :Session.objects.filter(is_active=True).first(),
        "page_title" :"Subject Performance (exam wise)",

      }
    return render(request, "acc_admin_template/subject_wise_performance.html",context)
def get_course_performance_graph(request):
    course_id = request.GET.get('course_id')
    session_id = request.GET.get('session_id')

    if not course_id or not session_id:
        return JsonResponse({'error': 'Missing course_id or session_id'})

    try:
        course = Course.objects.get(id=course_id)
        session = Session.objects.get(id=session_id)
    except (Course.DoesNotExist, Session.DoesNotExist):
        return JsonResponse({'error': 'Course or session not found'})

    exams = ExamtypeSettings.objects.all().order_by('id')
    labels = list(exams.values_list('exam_name', flat=True))

    # Include staff & subject relations
    subjects = Subject.objects.filter(course_id=course_id).select_related('staff', 'subject')

    datasets = []
    staff_groups = {}

    for sub in subjects:
        staff_groups.setdefault(sub.staff, []).append(sub)

    for staff, subject_objs in staff_groups.items():
        staff_data = []
        subject_ids = [s.id for s in subject_objs]

        # ✅ Get subject names safely (from the FK)
        subject_names = [
            getattr(s.subject, 'name', f"Subject {s.id}") for s in subject_objs
        ]

        for exam in exams:
            results = StudentResult.objects.filter(
                subject_id__in=subject_ids,
                session_id=session.id,
                exam_type_id=exam.id
            )

            avg_marks = 0
            if results.exists():
                total = 0
                count = 0
                for r in results:
                    try:
                        test_val = float(r.test) if r.test else 0
                        total += test_val
                        count += 1
                    except ValueError:
                        pass

                if count > 0:
                    avg_marks = total / count
                if exam.max_marks > 0:
                    avg_marks = (avg_marks / exam.max_marks) * 100

            staff_data.append(round(avg_marks, 2))

        # ✅ Staff name + subjects combined
        subject_text = ", ".join(subject_names)
        label_text = f"{staff.admin.first_name} {staff.admin.last_name} ({subject_text})"

        datasets.append({
            'label': label_text,
            'data': staff_data,
            'borderColor': random_color(),
            'backgroundColor': random_color(),
            'tension': 0.3,
            'fill': False,
            'pointRadius': 5,
        })

    return JsonResponse({
        'labels': labels,
        'datasets': datasets,
        'title': f"Staff Performance - {course.name} {course.division}"
    })

# Utility
def random_color():
    """Generate random hex color."""
    return "#%06x" % random.randint(0, 0xFFFFFF)

def get_subject_graph(request):
    subjectmaster_id = request.GET.get("subject_id")
    exam_id = request.GET.get("exam_id")
    session_id = request.GET.get("session_id")
    # print(subjectmaster_id,exam_id)
    # Subject Master Fetch
    submaster = Subjectmaster.objects.filter(id=subjectmaster_id).first()
   
    if not submaster:
        return JsonResponse({"error": "Subject not found"}, status=404)

  
    subject_variants = Subject.objects.filter(subject_id=subjectmaster_id).select_related("course")
    
    if not subject_variants.exists():
        return JsonResponse({"error": "No classes found for this subject"}, status=404)

    exam_obj = ExamtypeSettings.objects.filter(id=exam_id).first()
    max_marks = float(exam_obj.max_marks) if exam_obj else 0

    graph_data = []

  
    for sub in subject_variants:
        
        results = StudentResult.objects.filter(
            subject_id=sub.id,   # subject table id
            exam_type_id=exam_id,
            session_id=session_id
        ).select_related("student")

        if not results.exists():
            continue

        percentage_color_map = {}

        def get_color(percent):
            if percent in percentage_color_map:
                return percentage_color_map[percent]
            if percent >= 75:
                c = "#146b0cff"
            elif percent >= 60:
                c = "#28e141ff"
            elif percent >= 50:
                c = "#ffc107"
            elif percent >= 35:
                c = "#e3d10cff"
            else:
                c = "#f6061eff"
            percentage_color_map[percent] = c
            return c

        # Labels = exam names (always 1 exam = 1 label)
        labels = [exam_obj.exam_name]

        students_data = []

        student_ids = set(r.student_id for r in results)
        for sid in student_ids:
            stu = Student.objects.get(id=sid)
            r = results.filter(student_id=sid).first()

            marks = float(r.test) if r.test else 0
            percent = round((marks / max_marks) * 100, 2) if max_marks else 0

            students_data.append({
                "student_name": stu.admin.first_name,
                "marks": {
                    exam_obj.exam_name: {
                        "percentage": percent,
                        "color": get_color(percent)
                    }
                }
            })

        graph_data.append({
            "course_name": f"{sub.course.name}-{sub.course.division}",
            "subject_name": submaster.name,
            "labels": labels,
            "students": students_data
        })

    return JsonResponse({"subjects": graph_data})

# def alumni_add_alumini(request):
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
#             passport_url = None
#             if 'profile_pic' in request.FILES:
#                     passport = request.FILES['profile_pic']
#                     profile_storage = FileSystemStorage(
#                         location=os.path.join(settings.MEDIA_ROOT, 'profiles')
#                     )
#                     filename = profile_storage.save(passport.name, passport)
#                     passport_url = os.path.join('profiles', filename)

           
           


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
#                      return redirect(reverse('alumni_add_alumini'))
#             except Exception as e:
#                  messages.error(request, f"Could Not Add: {str(e)}")
#         else:
#             messages.error(request, "Please correct the following errors!")
#     return render(request,'acc_admin_template/alumini_template.html',context)
def alumni_manage_alumini(request):
    alumini = Alumnimembers.objects.all()
    form = AlumniMembersForm(request.POST or None,request.FILES or None)
    context = {
        'form' : form,
        'alumini': alumini,
        'page_title': 'Manage Alumini'
    }
    return render(request,'acc_admin_template/manage_alumini_template.html',context)
def alumni_add_alumini(request):
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
                    return redirect(reverse('alumni_add_alumini'))

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
                return redirect(reverse('alumni_add_alumini'))

            except Exception as e:
                traceback.print_exc()
                messages.error(request, f"Could not add alumni: {str(e)}")
        else:
            messages.error(request, "Form contains errors. Please correct them.")
    else:
        form = AlumniMembersForm()

    return render(request,'acc_admin_template/alumini_template.html',context={
        'form': form,
        'page_title': 'Add Alumni'
    })


def  alumni_manage_alumini(request):
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
    return render(request,'acc_admin_template/manage_alumini_template.html',context)


def alumni_events(request):
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
            return redirect(reverse('alumni_events'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = AlumniEventsForm()

    context = {
        'form': form,
        'page_title': 'Add Alumni Events'
    }
    return render(request, 'acc_admin_template/alumni_events_template.html',context)  

def  manage_alumnievents(request):
 event = AlumniEventsInfo.objects.all()
 context = {
        'event': event,
        'page_title': 'Manage  Alumni Events'
    }
 return render(request, 'acc_admin_template/manage_alumni_events_template.html',context )
   
def alumniedit_alumnievents(request,event_id):
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

    return render(request, 'acc_admin_template/edit_alumni_events_template.html',context ) 
def alumnidelete_alumnievents(request,event_id):
    event = get_object_or_404(AlumniEventsInfo, id=event_id)
    event.delete()
    messages.success(request, "Alumni Event Information is deleted successfully!")
    return redirect(reverse('manage_alumnievents')) 

def alumniedit_alumini(request,alumini_id):
     alumni = get_object_or_404(Alumnimembers, admin__id=alumini_id)
     user = alumni.admin

    # Save original email
     original_email = user.email

    # Create initial data from user fields
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

     form = AlumniMembersForm(request.POST or None, request.FILES or None, instance=alumni, initial=initial_data)

     context = {
        'form': form,
        'alumini_id': alumini_id,
        'page_title': 'Edit Alumni'
    }

     if request.method == 'POST':
        if form.is_valid():
            try:

                # Extract data
                # user.first_name = form.cleaned_data.get('first_name')
                # user.last_name = form.cleaned_data.get('last_name')
                new_email = form.cleaned_data.get('email')
                # user.gender = form.cleaned_data.get('gender')
                # user.city = form.cleaned_data.get('city')
                # user.state = form.cleaned_data.get('state')
                # user.district_name = form.cleaned_data.get('district_name')
                # user.country = form.cleaned_data.get('country')
                # user.street_address = form.cleaned_data.get('street_address')

                # Extract user details from the form
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.password = form.cleaned_data.get('password') or None
                user.gender = form.cleaned_data.get('gender')
                user.date_of_birth = form.cleaned_data.get('date_of_birth') # Added DOB
                user.city = form.cleaned_data.get('city')
                user.state = form.cleaned_data.get('state')
                user.district_name = form.cleaned_data.get('district_name')
                user.country = form.cleaned_data.get('country')
                user.street_address = form.cleaned_data.get('street_address')
                user.course = form.cleaned_data.get('course')
                user.mobile = form.cleaned_data.get('mobile')
                user.current_street_address = form.cleaned_data.get('current_street_address')
                user.current_city = form.cleaned_data.get('current_city')
                user.current_district_name = form.cleaned_data.get('current_district_name')
                user.current_state = form.cleaned_data.get('current_state')
                user.current_course = form.cleaned_data.get('current_course')
                user.current_department = form.cleaned_data.get('current_department')
                user.current_period_of_study = form.cleaned_data.get('current_period_of_study')
                user.employment_status = form.cleaned_data.get('employment_status')
                user.employment_remarks = form.cleaned_data.get('employment_remarks')
                employment_sectors = form.cleaned_data.get('employment_sectors')
                course_studied = form.cleaned_data.get('course_studied')
                on_campus_achievements = form.cleaned_data.get('on_campus_achievements')
                beyond_college_achievements = form.cleaned_data.get('beyond_college_achievements')
                outside_institution_course = form.cleaned_data.get('outside_institution_course')
                contribution = form.cleaned_data.get('contribution')
                mode_of_payment = form.cleaned_data.get('mode_of_payment')
                membershipfees = form.cleaned_data.get('membershipfees')
                willingness = form.cleaned_data.get('willingness')
                is_active = form.cleaned_data.get('is_active')

                passport = request.FILES.get('profile_pic')
                # Update email (after saving the old one above)
                user.email = new_email
                user.save()
                if passport:
                    save_user_profile_pic(passport, user)

                # Update alumni fields
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

                # ✅ If email changed, send mail to new email
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

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.ehlo()
                        server.starttls()
                        server.login('alumniimentor@gmail.com', 'lznjeuvbdpsozqim')  
                        server.send_message(msg)
                        server.quit()
                    except Exception as mail_error:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.exception('Error sending update email')
                        messages.warning(request, "Alumni updated, but email notification failed.")

                messages.success(request, "Alumni profile updated successfully.")
                return redirect(reverse('alumniedit_alumini', args=[alumini_id]))

            except Exception as e:
                messages.error(request, "Could not update alumni: " + str(e))
        else:
            messages.error(request, "Form contains errors. Please correct them.")
     return render(request,'acc_admin_template/alumniedit_alumini_template.html',context)

# def alumnidelete_alumini(request, alumini_id):
#     alumini = get_object_or_404(Alumnimembers, id=alumini_id)
#     alumini.delete()
#     messages.success(request, "Alumini deleted successfully!")
#     return redirect(reverse('alumni_manage_alumini'))

def alumnidelete_alumini(request, alumini_id):
    alumini = get_object_or_404(CustomUser, id=alumini_id)
    delete_user_profile_pic(alumini)
    alumini.delete()

    messages.success(request, "Alumini deleted successfully!")
    return redirect(reverse('alumni_manage_alumini'))

def add_careerguidanceprogrammes_alumni(request):
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
            return redirect(reverse('add_careerguidanceprogrammes_alumni'))
        else:
            messages.error(request, "Kindly ensure that all required fields in the form are completed accurately and in full.")
    else:
        form = CareerGuidanceForm()

    context = {
        'form': form,
        'page_title': 'Add Career Guidance Programme Details'
    }
    return render(request, 'acc_admin_template/add_careerguidanceprogrammes_alumni.html',context)
def  manage_careerguidanceprogrammes_alumni(request):
 programme = CareerGuidance.objects.all()
 context = {
        'programme': programme,
        'page_title': 'Manage  Career Guidance Programme Details'
    }
 return render(request,'acc_admin_template/manage_career_guidance_programme_alumni_template.html',context )

def edit_careerguidance_programme_alumni(request,programme_id):
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

    return render(request, 'acc_admin_template/edit_career_guidance_programme_alumni_template.html',context )  

def delete_careerguidance_programme_alumni(request,programme_id):
    programme = get_object_or_404(CareerGuidance, id=programme_id)
    programme.delete()
    messages.success(request, "Career Guidance Programme details deleted successfully!")
    return redirect(reverse('manage_careerguidanceprogrammes_alumni')) 

@csrf_exempt
def alumni_students_list2(request):
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
        "employment_status","employment_remarks","employment_sectors", "is_active", "course__name","admin__first_name", "admin__last_name", "admin__email","admin__id", "admin__profile_pic"
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


