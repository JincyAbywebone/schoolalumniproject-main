"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from main_app.video_serve import serve_video

# from main_app.EditResultView import EditResultView

from .import hod_views, staff_views, student_views, views, acc_admin_views,super_views,parent_views,alumniadmin_views,alumni_views
from .import hod_views, staff_views, student_views, views, acc_admin_views,super_views,parent_views,alumniadmin_views,alumni_views
# from .import hod_views, staff_views, student_views, views,alumni_views, acc_admin_views,alumni_views, alumniadmin_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
#     path("user_logout/", views.user_logout, name='user_logout'),
    path("signup/", views.signup, name='signup'),
    path("verify_otp/", views.verify_otp, name='verify_otp'),
    path("dashboard_login/", views.dashboard_login, name='dashboard_login'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("course/add", hod_views.add_course, name='add_course'),
     path('admin/academic_alumni_settings/', hod_views.academic_alumni_settings, name='academic_alumni_settings'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin/admin_notify_parent", hod_views.admin_notify_parent,
         name='admin_notify_parent'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave,
         name="view_student_leave",),

    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave"),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
     path('acc_admin/get_student_bargraph/', acc_admin_views.get_student_bargraph, name='acc_admin_get_student_bargraph'),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("school/add_school", hod_views.add_school, name='add_school'),
    path("school/manage_school", hod_views.manage_school, name='manage_school'),
    path("school/edit_school/<int:school_id>", hod_views.edit_school, name='edit_school'),
    path("school/delete_school/<int:school_id>", hod_views.delete_school, name='delete_school'),
    path('students/', hod_views.students_list, name='students_list'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         hod_views.edit_student, name='edit_student'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),
     path("view_subject_result",
           hod_views.view_filtered_class_results_by_subject, name="view_subject_result"),

     path("alumini/add_alumini",hod_views.add_alumini, name='add_alumini'),
     path("alumini/manage_alumini",hod_views.manage_alumini, name='manage_alumini'),
     path("alumini/edit_alumini/<int:alumini_id>",hod_views.edit_alumini, name='edit_alumini'),
     path("alumni/alumni_students_list/", hod_views.alumni_students_list, name="alumni_students_list"),
     path("alumini/delete_alumini/<int:alumini_id>",hod_views.delete_alumini, name='delete_alumini'),
     path("alumini/upload_alumini",hod_views.upload_alumni_data, name='upload_alumini'),
     path('alumini/approve_alumni/', hod_views.approve_alumini, name="approve_alumni"),
     path("alumni/add_alumni_admin", hod_views.add_alumni_admin, name='add_alumni_admin'),
     path("alumni/manage_alumni_admin/", hod_views.manage_alumni_admin, name='manage_alumni_admin'),
     path("admin/search/", hod_views.search, name='search'),
    
      #Alumni Admin
     path('alumni_admin/alumniadmin_home/', alumniadmin_views.alumniadmin_home, name='alumniadmin_home'),  # name MUST match
     path("alumni_admin/add_alumni1",alumniadmin_views.add_alumni1, name='add_alumni1'),
     path("alumni_admin/manage_alumni1",alumniadmin_views.manage_alumni1, name='manage_alumni1'),
     

     path('alumni_admin/edit_alumniAdmin/<int:allAdmin>/', hod_views.edit_alumniAdmin, name='edit_alumniAdmin'),
     path("alumni/delete_alumni_admin/<int:allAdmin_id>", hod_views.delete_alumni_admin, name='delete_alumni_admin'),

     path('alumni_admin/alumniadminviewprofile/', alumniadmin_views.alumniadminviewprofile, name='alumniadminviewprofile'),
     
     path("alumni_admin/alumniexcel_form/", alumniadmin_views.alumniexcel_form, name='alumniexcel_form'),
     # path("alumni_admin/alumni_excel_data",alumniadmin_views.alumni_excel_data, name='alumni_excel_data'),
     path("alumni_admin/upload_alumni_excel",alumniadmin_views.upload_alumni_excel, name='upload_alumni_excel'),
     path("alumni_admin/add_jobpostings1/",alumniadmin_views.add_jobpostings1, name='add_jobpostings1'),
     path("alumni_admin/manage_jobpostings1",alumniadmin_views.manage_jobpostings1, name='manage_jobpostings1'),
     path("alumni_admin/add_companies1",alumniadmin_views.add_companies1, name='add_companies1'),

     path("alumni_admin/manage_companies1",alumniadmin_views.manage_companies1, name='manage_companies1'),
     path("alumni_admin/add_alumni_events1/",alumniadmin_views.add_alumni_events1, name='add_alumni_events1'),

     path("alumni_admin/manage_alumnievents1/",alumniadmin_views.manage_alumnievents1, name='manage_alumnievents1'),
     
     path("alumni_admin/add_careerguidanceprogrammes1/",alumniadmin_views.add_careerguidanceprogrammes1, name='add_careerguidanceprogrammes1'),
     path("alumni_admin/manage_careerguidanceprogrammes1/",alumniadmin_views.manage_careerguidanceprogrammes1, name='manage_careerguidanceprogrammes1'),
     # path("alumni_admin/create_alumni_chatgroup1/",alumniadmin_views.create_alumni_chatgroup1, name='create_alumni_chatgroup1'),
     # path("alumni_admin/manage_alumni_chatgroup1/",alumniadmin_views.manage_alumni_chatgroup1, name='manage_alumni_chatgroup1'),
     # path("alumni_admin/add_member_to_group/",alumniadmin_views.add_member_to_group, name='add_member_to_group'),
     path("alumini/get_alumini_course/" ,alumniadmin_views.get_alumini_course,name='get_alumini_course'),
     path('alumni_admin/viewfeedbacks',alumniadmin_views.viewalumnifeedback,name="viewfeedbacks"),
     path("alumni_admin/alumni_print/", alumniadmin_views.alumni_print, name='alumni_print'),
     path("alumni_admin/alumni_search_list/", alumniadmin_views.alumni_search_list, name='alumni_search_list'),
     path('alumni_admin/approve_alumnis/', alumniadmin_views.approve_alumini, name="approve_alumnis"),
     path("alumni_admin/alumni_students_list",alumniadmin_views.alumni_students_list, name='alumni_students_list'),
     path("alumni_admin/edit_manage_alumini/<int:alumini_id>", alumniadmin_views.edit_manage_alumini, name='edit_manage_alumini'),
     path("alumni_admin/edit_alumini/<int:alumini_id>",alumniadmin_views.edit_alumini, name='alumni_admin_edit_alumini'),
     path("alumni_admin/deletealumini/<int:alumini_id>",alumniadmin_views.deletealumini, name='deletealumini'),
     path("alumni_admin/editjobpostings/<int:jobposting_id>",alumniadmin_views.editjobpostings, name='editjobpostings'),
     path("alumni_admin/deletejobpostings/<int:jobposting_id>",alumniadmin_views.deletejobpostings, name='deletejobpostings'),
     path("alumni_admin/editcompany/<int:company_id>",alumniadmin_views.editcompany, name='editcompany'),
     # path("alumni/edit_company/<int:company_id>",hod_views.edit_company, name='edit_company'),
     path("alumni_admin/guidecareer/<int:programme_id>",alumniadmin_views.guidecareer, name='guidecareer'),
     path("alumni/edit_alumnievents/<int:event_id>",alumniadmin_views.edit_alumnievents, name='edit_alumnievents'),
     path("alumni_admin/deletealumnievents/<int:event_id>",alumniadmin_views.deletealumnievents, name='deletealumnievents'),
     path("alumni_admin/delete_career/<int:programme_id>",alumniadmin_views.delete_career, name='delete_career'),
     path("alumni_admin/deletecompany/<int:company_id>",alumniadmin_views.deletecompany, name='deletecompany'),
     path("alumni_admin/alumniexceldata/",alumniadmin_views.alumniexceldata, name='alumniexceldata'),
     
     path("alumni_admin/delete_allAdmin/<int:allAdmin_id>", hod_views.delete_allAdmin, name='delete_allAdmin'),
   # alumni


     path("fees/fee_settings",
         hod_views.fee_settings, name='fee_settings'),
     path("fees/manage_fee_settings",
         hod_views.manage_fee_settings, name='manage_fee_settings'),
     path("fees/edit_fee_settings/<int:fee_id>/",
         hod_views.edit_fee_settings, name='edit_fee_settings'),
     path("fees/delete_fee_settings/<int:fee_id>/",
         hod_views.delete_fee_settings, name='delete_fee_settings'),
         path("fees/add_fee_amount_settings",
         hod_views.add_fee_amount_settings, name='add_fee_amount_settings'),
     path("fees/get_feeamountsettings",
         hod_views.get_feeamountsettings, name='get_feeamountsettings'),
     path("fees/manage_fee_amount_settings",
         hod_views.manage_fee_amount_settings, name='manage_fee_amount_settings'),   
     path('fees/edit_fee_amount/<int:fee_id>/', 
          hod_views.edit_fee_amount, name='edit_fee_amount'),
     path('fees/delete_fee_amount/<int:fee_id>/', 
          hod_views.delete_fee_amount, name='delete_fee_amount'),
     path('ajax/get-email-by-name/', hod_views.get_email_by_name, name='get_email_by_name'),
     path('ajax/get-students-by-course/', hod_views.get_students_by_course, name='get_students_by_course'),    
     path("view_class_result/",
           hod_views.view_filtered_class_results, name="view_class_result"),
     path('ajax/get-email-by-name/', hod_views.get_email_by_name, name='get_email_by_name'),
     path('acc_admin/edit_allAdmin/<int:allAdmin>/', hod_views.edit_allAdmin, name='edit_allAdmin'),
     path('acc_admin/delete_allAdmin/<int:allAdmin>/', hod_views.delete_allAdmin, name='delete_allAdmin'),
     path('admin/admin_studentgraph/', hod_views.admin_studentgraph, name='admin_studentgraph'),
     path('admin/get_student_marks/', hod_views.get_student_marks, name='get_student_marks'),
     path('admin_result/get_subjects/', hod_views.get_subjects, name='get_subjects'),
      path('admin/get_student/', hod_views.get_student, name='get_student'),
     # path("curriculam/admin_bulk_result",hod_views.admin_bulk_result,name='admin_bulk_result'),
     path("curriculam/admin_bulk_result_new",hod_views.admin_bulk_result_new,name='admin_bulk_result_new'),
     path("admin_result/new_student_result", hod_views.new_student_result, name='new_student_result'),
     # path("leave/take_teacher_attendance",
     #     hod_views.take_teacher_attendance, name='take_teacher_attendance'),
     path("admin_result/save_student_results_new1", hod_views.save_student_results_new1, name='save_student_results_new1'),
     path("admin_result/get_students_bulk1", hod_views.get_students_bulk1, name='get_students_bulk1'),
     path("admin_result/get_term_list", hod_views.get_term_list, name='get_term_list'),
     path("admin_result/manage_bulk_result_new", hod_views.manage_bulk_result_new, name='manage_bulk_result_new'),
     path("admin_result/edit_bulkresult/<int:result_id>", hod_views.edit_bulkresult, name='edit_bulkresult'),    
     path("admin_result/get_course_lists",hod_views.get_course_list,name='get_course_lists'),
     path('admin_result/update_student_result_new/<int:result_id>/', hod_views.update_student_result_new, name='update_student_result_new'),
     path("admin_result/delete_bulkresult/<int:result_id>", hod_views.delete_bulkresult, name='delete_bulkresult'),
     path("admin_result/admin_bulk_student_data", hod_views.admin_bulk_student_data, name='admin_bulk_student_data'),
     path('admin_result/subject_class_result', hod_views.subject_class_result, name='subject_class_result'),
     path('admin_result/admin_studentgraph/', hod_views.admin_studentgraph, name='admin_studentgraph'),
     path('api/exam-type-colors/', hod_views.get_exam_type_colors_new, name='get_exam_type_colors'),
     path('admin_result/admin_studentexamgraph/', hod_views.admin_studentexamgraph, name='admin_studentexamgraph'),
     path('admin/get_student_bargraph/', hod_views.get_student_bargraph, name='get_student_bargraph'),
     path("admin_result/get-max-mark/", hod_views.get_max_mark, name="get_max_mark"),
     path("admin/search/", hod_views.search, name="search"),
     path("admin/student_search_list/",hod_views.student_search_list,name="student_search_list"),
     path('admin/add_parent/', hod_views.add_parent, name='add_parent'),
     path('admin/manage_parent/', hod_views.manage_parent, name='manage_parent'),
     path('admin/edit_parent/<int:parent_id>/', hod_views.edit_parent, name='edit_parent'),
     path('admin/delete_parent/<int:parent_id>/', hod_views.delete_parent, name='delete_parent'),
     path('admin/approve-notification/<int:id>/', hod_views.approve_notification, name='approve_notification'),
     path("staff_result/staff_bulk_student_data1", hod_views.staff_bulk_student_data1, name='staff_bulk_student_data1'),


    #alumni
     path("alumni/add_alumni_events/",hod_views.add_alumni_events, name='add_alumni_events'),
     path("alumni/manage_alumni_events/",hod_views.manage_alumni_events, name='manage_alumni_events'),
     path("alumni/edit_alumnievents/<int:event_id>",hod_views.edit_alumnievents, name='edit_alumnievents'),
     path("alumni/delete_alumnievents/<int:event_id>",hod_views.delete_alumnievents, name='delete_alumnievents'),
     path("alumni/add_careerguidanceprogrammes/",hod_views.add_careerguidanceprogrammes, name='add_careerguidanceprogrammes'),
      path("alumni/manage_careerguidanceprogrammes/",hod_views.manage_careerguidanceprogrammes, name='manage_careerguidanceprogrammes'),
     path("alumni/edit_careerguidance_programme/<int:programme_id>",hod_views.edit_careerguidance_programme, name='edit_careerguidance_programme'),
      path("alumni/delete_careerguidance_programme/<int:programme_id>",hod_views.delete_careerguidance_programme, name='delete_careerguidance_programme'),
    
    
      #Accademic Admin
     
     
     path("acc_admin/add", hod_views.add_acc_admin, name='add_acc_admin'),
     path("acc_admin/manage/", hod_views.manage_acc_admin, name='manage_acc_admin'),
     path("acc_admin/home/", acc_admin_views.acc_admin_home, name='acc_admin_home'), 
     path("curriculam/add_curriculam", acc_admin_views.add_curriculam, name='add_curriculam'),
     path("curriculam/get_course" ,acc_admin_views.get_course,name='get_course'),
     path("curriculam/get_curriculam" ,acc_admin_views.get_curriculam,name='get_curriculam'),
     path("curriculam/manage_curriculam" ,acc_admin_views.manage_curriculam,name='manage_curriculam'),
     path("curriculam/edit_curriculam/<int:id>" ,acc_admin_views.edit_curriculam,name='edit_curriculam'),
     path("curriculam/delete_curriculam/<int:id>" ,acc_admin_views.delete_curriculam,name='delete_curriculam'),
     # path("curriculam/view_curriculam/<int:id>" ,acc_admin_views.view_curriculam,name='view_curriculam'),
    path("curriculam/get_teachers" ,acc_admin_views.get_teachers , name='get_teachers'),
    path("curriculam/add_subject_master" ,acc_admin_views.add_subject_master,name='add_subject_master'),
    path("curriculam/manage_subject_master" ,acc_admin_views.manage_subject_master,name='manage_subject_master'),
    path("curriculam/edit_subjectmaster/<int:id>" ,acc_admin_views.edit_subjectmaster,name='edit_subjectmaster'),
    path("curriculam/delete_subjectmaster/<int:id>" ,acc_admin_views.delete_subjectmaster,name='delete_subjectmaster'),
    path("curriculam/add_department" ,acc_admin_views.add_department,name='add_department'),
    path("curriculam/manage_department" ,acc_admin_views.manage_department,name='manage_department'),
    path("curriculam/edit_department/<int:id>" ,acc_admin_views.edit_department,name='edit_department'),
    path("curriculam/delete_department/<int:id>" ,acc_admin_views.delete_department,name='delete_department'),
    path("curriculam/academic_add_result" ,acc_admin_views.academic_add_result,name='academic_add_result'),
    path("curriculam/get_students_list",acc_admin_views.get_students_list,name='get_students_list'),
    path("curriculam/upload_excel",acc_admin_views.upload_excel,name='upload_excel'),
    path("curriculam/get_students_bulk",acc_admin_views.get_students_bulk,name='get_students_bulk'),
    path("curriculam/academic_bulk_result",acc_admin_views.academic_bulk_result,name='academic_bulk_result'),
    path("curriculam/get_course_list",acc_admin_views.get_course_list,name='get_course_list'),
    path("curriculam/student_excelform",acc_admin_views.student_excelform,name='student_excelform'),
    path("curriculam/student_excelform2",acc_admin_views.student_excelform2,name='student_excelform2'),
    path("curriculam/upload_student_data2/", acc_admin_views.upload_student_data2, name='upload_student_data2'),
    path("curriculam/student_excel_data",acc_admin_views.student_excel_data,name='student_excel_data'),
    path("curriculam/student_excel_data2",acc_admin_views.student_excel_data2,name='student_excel_data2'),
    path("curriculam/upload_student_data/", acc_admin_views.upload_student_data, name='upload_student_data'),
    path("curriculam/academic_admin_view_profile/", acc_admin_views.academic_admin_view_profile, name='academic_admin_view_profile'),
    path("curriculam/send_notification/<int:id>", acc_admin_views.send_notification, name='send_notification'),
    path('curriculam/save_student_results/', acc_admin_views.save_student_results, name='save_student_results'), 
    path("curriculam/save_excel_data/<int:course>/<int:subject_data1>/",acc_admin_views.save_excel_data,name='save_excel_data'),
    path("curriculam/manage_curriculam_data/",acc_admin_views.manage_curriculam_data,name='manage_curriculam_data'),
    path("acc_admin_view_class_result/",acc_admin_views.view_filtered_class_results, name="acc_admin_view_class_result"),
    path("acc_admin_view_subject_result", acc_admin_views.view_filtered_class_results_by_subject, name="acc_admin_view_subject_result"),
    path('add_examtype_settings/', acc_admin_views.add_examtype_settings, name='add_examtype_settings'),
    path('manage_examtype_settings/', acc_admin_views.manage_examtype_settings, name='manage_examtype_settings'),
    path('edit_examtype_settings/<int:id>/', acc_admin_views.edit_examtype_settings, name='edit_examtype_settings'),
    path('delete_examtype_settings/<int:id>/', acc_admin_views.delete_examtype_settings, name='delete_examtype_settings'),
    path("acc_admin/get_term_list", acc_admin_views.get_term_list, name='get_term_list'),
    path("acc_admin/manage_bulk_result", acc_admin_views.manage_bulk_result, name='manage_bulk_result'),
    path("acc_admin/bulk_student_data", acc_admin_views.bulk_student_data, name='bulk_student_data'),
    path("acc_admin/edit_bulkresult/<int:result_id>", acc_admin_views.edit_bulkresult, name='edit_bulkresult'),
    path("acc_admin/delete_bulkresult/<int:result_id>", acc_admin_views.delete_bulkresult, name='delete_bulkresult'),
    path('acc_admin/get_exams_by_term', acc_admin_views.get_exams_by_term, name='get_exams_by_term'),
    path('acc_admin/new_class_result', acc_admin_views.new_class_result, name='new_class_result'),
    path('acc_admin/update_student_bulk_result/<int:result_id>/', acc_admin_views.update_student_bulk_result, name='update_student_bulk_result'),
    path('acc_admin/acc_admin_studentgraph/', acc_admin_views.acc_admin_studentgraph, name='acc_admin_studentgraph'),
    path('acc_admin/acc_admin_studentexamwisegraph/',acc_admin_views.acc_admin_studentexamwisegraph,name='acc_admin_studentexamwisegraph'),
    path('acc_admin/get_subject/', acc_admin_views.get_subject, name='get_subject'),
    path('acc_admin/get_student/', acc_admin_views.get_student, name='get_student'),
    path('acc_admin/get_studentmarks1/', acc_admin_views.get_studentmarks1, name='get_studentmarks1'),
    path('acc_admin/acc_staffgraph/', acc_admin_views.acc_admin_staffgraph, name='acc_staffgraph'),

    path('acc_admin/get_staff/', acc_admin_views.get_staff, name='get_staff'),
    path('acc_admin/get_subject_staff/', acc_admin_views.get_subject_staff, name='get_subject_staff'),
    path('acc_admin/get_staff_graph/', acc_admin_views.get_staff_graph, name='get_staff_graph'),
    path("acc_admin/get_course_lists",acc_admin_views.get_course_list,name='get_course_lists'),
    path("acc_admin/get_max_mark/", acc_admin_views.getmaxmarks, name="get_max_mark"),
    path("acc_admin/save_student_results_new", acc_admin_views.save_student_results, name='save_student_results_new'),
    path('acc_admin/get_subjects/', acc_admin_views.get_subjects, name='get_subjects'),
    path('acc_admin/get_student/', acc_admin_views.get_student, name='get_student'),
    path('api/examtypecolors/', acc_admin_views.examtypecolors, name='examtypecolors'),
    path('acc_admin/academic_admin_studentexamgraph/', acc_admin_views.academic_admin_studentexamgraph, name='academic_admin_studentexamgraph'),
    path('acc_admin/acc_admin_staffgraph2/', acc_admin_views.acc_admin_staffgraph2, name='acc_admin_staffgraph2'),
    path('acc_admin/get_student_pie_data/', acc_admin_views.get_student_pie_data, name='get_student_pie_data'),
    path('acc_admin/classwise_examreport/', acc_admin_views.classwise_examreport, name='classwise_examreport'),
    path('acc_admin/get_staff_graphmark/', acc_admin_views.get_staff_graphmark, name='get_staff_graphmark'),
    path('acc_admin/teachers_list/', acc_admin_views.teachers_list, name='teachers_list'),
    path('acc_admin/update-permission/', acc_admin_views.update_permission, name='update_permission'),
    path('acc_admin/acc_admin_averagemark/', acc_admin_views.acc_admin_averagemark, name='acc_admin_averagemark'),
    path('acc_admin/get_staff_average/', acc_admin_views.get_staff_average, name='get_staff_average'),
    path("acc_admin/alumni_students_list2/", acc_admin_views.alumni_students_list2, name="alumni_students_list2"),

     # AccAdmin LMS (View Only)
     path('acc_admin/lms/dashboard/', acc_admin_views.acc_admin_lms_dashboard, name='acc_admin_lms_dashboard'),
     path('acc_admin/lms/videos/', acc_admin_views.acc_admin_view_lms_videos, name='acc_admin_view_lms_videos'),
     path('acc_admin/lms/images/', acc_admin_views.acc_admin_view_lms_images, name='acc_admin_view_lms_images'),
     path('acc_admin/lms/notes/', acc_admin_views.acc_admin_view_lms_notes, name='acc_admin_view_lms_notes'),


    path('acc_admin/staff_performance/', acc_admin_views.staff_performance, name='staff_performance'),
    path('acc_admin/subject_performance/', acc_admin_views.subject_performance, name='subject_performance'),

    path('acc_admin/get_course_performance_graph/', acc_admin_views.get_course_performance_graph, name='get_course_performance_graph'),
     path("acc_admin/alumni_add_alumini",acc_admin_views.alumni_add_alumini, name='alumni_add_alumini'),
    path("acc_admin/alumni_manage_alumini",acc_admin_views.alumni_manage_alumini, name='alumni_manage_alumini'),
    path("acc_admin/alumni_events",acc_admin_views.alumni_events, name='alumni_events'),
    path("acc_admin/manage_alumnievents",acc_admin_views.manage_alumnievents, name='manage_alumnievents'),
    path("acc_admin/alumniedit_alumnievents/<int:event_id>",acc_admin_views.alumniedit_alumnievents, name='alumniedit_alumnievents'),
    path("acc_admin/alumnidelete_alumnievents/<int:event_id>",acc_admin_views.alumnidelete_alumnievents, name='alumnidelete_alumnievents'),
    path("acc_admin/alumniedit_alumini/<int:alumini_id>",acc_admin_views.alumniedit_alumini, name='alumniedit_alumini'),
    path("acc_admin/alumnidelete_alumini/<int:alumini_id>",acc_admin_views.alumnidelete_alumini, name='alumnidelete_alumini'),
    path("acc_admin/add_careerguidanceprogrammes_alumni",acc_admin_views.add_careerguidanceprogrammes_alumni, name='add_careerguidanceprogrammes_alumni'),
    path("acc_admin/manage_careerguidanceprogrammes_alumni",acc_admin_views.manage_careerguidanceprogrammes_alumni, name='manage_careerguidanceprogrammes_alumni'),
    path("acc_admin/edit_careerguidance_programme_alumni/<int:programme_id>",acc_admin_views.edit_careerguidance_programme_alumni, name='edit_careerguidance_programme_alumni'),
    path("acc_admin/delete_careerguidance_programme_alumni/<int:programme_id>",acc_admin_views.delete_careerguidance_programme_alumni, name='delete_careerguidance_programme_alumni'),
    
    

     path('acc_admin/get_course_performance_graph/', acc_admin_views.get_course_performance_graph, name='get_course_performance_graph'),

      # Student Promotion - Super Admin (HOD)
    
    
    
     path('admin/student_promotion/', hod_views.student_promotion, name='student_promotion'),
     path('admin/promotion_history/', hod_views.promotion_history, name='promotion_history'),
     path('admin/get_promotion_students/', hod_views.get_promotion_students, name='get_promotion_students'),
     path('admin/promote_students/', hod_views.promote_students, name='promote_students'),
     path('admin/promotion_detail/<int:pk>/', hod_views.promotion_detail, name='promotion_detail'),
     path('admin/undo_promotion/<int:promotion_id>/', hod_views.undo_promotion, name='undo_promotion'),
     path('admin/export_promotion_pdf/<int:from_session_id>/<int:to_session_id>/<int:from_course_id>/<int:to_course_id>/', hod_views.export_promotion_pdf, name='export_promotion_pdf'),
    path("get_subject_graph/", acc_admin_views.get_subject_graph, name="get_subject_graph"),
   
     # Student Promotion - Academic Admin
     path('acc_admin/student_promotion/', acc_admin_views.acc_admin_student_promotion, name='acc_admin_student_promotion'),
     path('acc_admin/promotion_history/', acc_admin_views.acc_admin_promotion_history, name='acc_admin_promotion_history'),
     path('acc_admin/get_promotion_students/', acc_admin_views.acc_admin_get_promotion_students, name='acc_admin_get_promotion_students'),
     path('acc_admin/promote_students/', acc_admin_views.acc_admin_promote_students, name='acc_admin_promote_students'),
     path('acc_admin/promotion_detail/<int:pk>/', acc_admin_views.acc_admin_promotion_detail, name='acc_admin_promotion_detail'),
     path('acc_admin/undo_promotion/<int:promotion_id>/', acc_admin_views.acc_admin_undo_promotion, name='acc_admin_undo_promotion'),
     path('acc_admin/export_promotion_pdf/<int:from_session_id>/<int:to_session_id>/<int:from_course_id>/<int:to_course_id>/', acc_admin_views.acc_admin_export_promotion_pdf, name='acc_admin_export_promotion_pdf'),

     # Transfer Certificate
     path('admin/transfer_certificate/', hod_views.issue_transfer_certificate, name='issue_transfer_certificate'),
     path('admin/get_tc_students/', hod_views.get_tc_students, name='get_tc_students'),
     path('admin/issue_tc/', hod_views.issue_tc, name='issue_tc'),
     path('admin/transfer_certificate_list/', hod_views.transfer_certificate_list, name='transfer_certificate_list'),
     path('admin/transfer_certificate_detail/<int:tc_id>/', hod_views.transfer_certificate_detail, name='transfer_certificate_detail'),
     path('admin/print_transfer_certificate/<int:tc_id>/', hod_views.print_transfer_certificate, name='print_transfer_certificate'),
     path('admin/reprint_transfer_certificate/<int:tc_id>/', hod_views.reprint_transfer_certificate, name='reprint_transfer_certificate'),
     # path('admin/bulk_transfer_certificate/', hod_views.bulk_transfer_certificate, name='bulk_transfer_certificate'),
     path('admin/print_transfer_certificate_register/', hod_views.print_transfer_certificate_register, name='print_transfer_certificate_register'),
     path('admin/cancel_transfer_certificate/', hod_views.cancel_transfer_certificate, name='cancel_transfer_certificate'),

    # Staff

    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance,
         name='staff_update_attendance'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance,
         name='get_student_attendance'),
    path("staff/attendance/save/",
         staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/",
         staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path("staff/result/staff_add_result2/", staff_views.staff_add_result2, name='staff_add_result2'),
    #     path("staff/result/edit/", EditResultView.as_view(),
    #          name='edit_student_result'),

    path("staff/result/manage_student_result/", staff_views.manage_student_result, name='manage_student_result'),
   path("staff/result/manage_student_result_new/", staff_views.manage_student_result_new, name='manage_student_result_new'),
  
  
    path('staff/result/fetch/', staff_views.fetch_student_result,
         name='fetch_student_result'),
     # path("staff/result/manage_result>",staff_views.manage_result,name='manage_result'),

     path("staff/result/select_termwise",staff_views.select_termwise,name='select_termwise'),

    path('staff/curriculam/view/', staff_views.staff_curriculam,
         name='staff_curriculam'),
     path("staff/curriculam/view/tick_status",staff_views.tick_status,name='tick_status'),
     path("staff/edit_staff_leave/<int:leave_id>",staff_views.edit_staff_leave,name='edit_staff_leave'),
     path("staff/delete_staff_leave/<int:leave_id>",staff_views.delete_staff_leave,name='delete_staff_leave'),
     path("staff/edit_result/<int:id>",staff_views.edit_result,name='edit_result'),
     path("staff/delete_result/<int:id>",staff_views.delete_result,name='delete_result'),
     path("staff/result/staff_get_course",staff_views.staff_get_course,name='staff_get_course'),
     path("staff/lesson/lesson_notes",staff_views.lesson_notes,name='lesson_notes'),
     path("staff/lesson/manage_lesson_notes",staff_views.manage_lesson_notes,name='manage_lesson_notes'),
     path("staff/lesson/edit_lesson_note/<int:id>",staff_views.edit_lesson_note,name='edit_lesson_note'),
     path("staff/lesson/delete_lesson_note/<int:id>",staff_views.delete_lesson_note,name='delete_lesson_note'),
     path("staff/lesson/staff_get_curriculam",staff_views.staff_get_curriculam,name='staff_get_curriculam'),
     # path("staff_view_class_result/",staff_views.view_filtered_class_results, name="staff_view_class_result"),
     path("staff_view_subject_result", staff_views.view_filtered_class_results_by_subject, name="staff_view_subject_result"),
     path("curriculam/staff_bulk_result",staff_views.staff_bulk_result,name='staff_bulk_result'),
     path("curriculam/staff_bulk_result_new",staff_views.staff_bulk_result_new,name='staff_bulk_result_new'),
     path("staff_result/staff_manage_bulk_result", staff_views.staff_manage_bulk_result, name='staff_manage_bulk_result'),

     path("staff_result/staff_manage_bulk_result_new", staff_views.staff_manage_bulk_result_new, name='staff_manage_bulk_result_new'),
     path("staff_result/staff_bulk_student_data", staff_views.staff_bulk_student_data, name='staff_bulk_student_data'),

     path("staff_result/staff_edit_bulkresult/<int:result_id>", staff_views.staff_edit_bulkresult, name='staff_edit_bulkresult'),
     path('staff_result/update_student_result/<int:result_id>/', staff_views.update_student_result, name='update_student_result'),
     path("staff_result/delete_bulkresult/<int:result_id>", staff_views.delete_bulkresult, name='delete_bulkresult'),
     path("staff/staff_view_filtered_class_results/",staff_views.view_filtered_class_results, name="staff_view_filtered_class_results"),
     path('staff/staff_new_class_result', staff_views.new_class_result, name='staff_new_class_result'),
     path('staff/staff_studentgraph/', staff_views.staff_studentgraph, name='staff_studentgraph'),
     path('staff/get_subject/', staff_views.get_subject, name='get_subject'),
    path('staff/get_student/', staff_views.get_student, name='get_student'),
    path('staff/get_student_marks/', staff_views.get_student_marks, name='get_student_marks'),
     # path("staff/lesson/add_lesson_notes", staff_views.add_lesson_notes, name='add_lesson_notes'),
     path('staff/staff_studentexamgraph/', staff_views.staff_studentexamgraph, name='staff_studentexamgraph'),
     path('staff/get_student_bargraph/', staff_views.get_student_bargraph, name='get_student_bargraph'),
     path('staff/staff_add_result_new/', staff_views.staff_add_result_new, name='staff_add_result_new'),
     # path('staff/add_alumini/', staff_views.add_alumini, name='add_alumni'),
     path('staff/get_students_result/', staff_views.get_students_result, name='get_students_result'),
     path("staff/get-max-marks/", staff_views.get_max_marks, name="get_max_marks"),
     path('api/exam-type/', staff_views.get_exam_type_colors, name='get_exam_type'),
     path("staff/get_course_list",staff_views.get_course_list,name='get_course_list'),
     path("staff/save_student_results", staff_views.save_student_results, name='save_student_results'),
     path("staff/get_term_list", staff_views.get_term_list, name='get_term_list'),
     path("staff/get_student_marks", staff_views.get_student_marks, name='get_student_marks'),
     path("staff/staff_studentexamreport", staff_views.staff_studentexamreport, name='staff_studentexamreport'),
     path("reports/student/<int:student_id>/<int:exam_type_id>/",staff_views.generate_student_report_pdf, name="student_report_pdf"),
     path('api/examtypecolors/', staff_views.examtypecolors, name='examtypecolors'),
     path('staff/staff_bulk_result_permissions/', staff_views.staff_bulk_result_permissions, name='staff_bulk_result_permissions'),

     # Staff LMS
     path('staff/lms/dashboard/', staff_views.staff_lms_dashboard, name='staff_lms_dashboard'),
     path('staff/lms/video/add/', staff_views.staff_add_lms_video, name='staff_add_lms_video'),
     path('staff/lms/videos/', staff_views.staff_manage_lms_videos, name='staff_manage_lms_videos'),
     path('staff/lms/video/view/<int:id>/', staff_views.staff_view_lms_video, name='staff_view_lms_video'),
     path('staff/lms/video/edit/<int:id>/', staff_views.staff_edit_lms_video, name='staff_edit_lms_video'),
     path('staff/lms/video/delete/<int:id>/', staff_views.staff_delete_lms_video, name='staff_delete_lms_video'),
     path('staff/lms/image/add/', staff_views.staff_add_lms_image, name='staff_add_lms_image'),
     path('staff/lms/images/', staff_views.staff_manage_lms_images, name='staff_manage_lms_images'),
     path('staff/lms/image/edit/<int:id>/', staff_views.staff_edit_lms_image, name='staff_edit_lms_image'),
     path('staff/lms/image/delete/<int:id>/', staff_views.staff_delete_lms_image, name='staff_delete_lms_image'),
     path('staff/lms/note/add/', staff_views.staff_add_lms_note, name='staff_add_lms_note'),
     path('staff/lms/notes/', staff_views.staff_manage_lms_notes, name='staff_manage_lms_notes'),
     path('staff/lms/note/edit/<int:id>/', staff_views.staff_edit_lms_note, name='staff_edit_lms_note'),
     path('staff/lms/note/delete/<int:id>/', staff_views.staff_delete_lms_note, name='staff_delete_lms_note'),
     path('staff/get_studentmarks1/', staff_views.get_studentmarks1, name='get_studentmarks1'),




    #super admin
     path('super_admin/dashboard_home/', super_views.dashboard_home, name='dashboard_home'),
     path('super_admin/academic_module/<str:module_code>/', super_views.academic_module, name='academic_module'),
    # path('super_admin/academic_module/<str:module_code>/', super_views.academic_module, name='academic_module'),
     
     path('super_admin/super_home/', super_views.super_home, name='super_home'),
     



     # Parent
    
     path('parent/home/', parent_views.parent_home, name='parent_home'),
     path('parent/student/<int:student_id>/', parent_views.parent_student_detail, name='parent_student_detail'),
     path('parent/submit-student-notification/', parent_views.submit_student_notification, name='submit_student_notification'),
     path('parent/student_search/', parent_views.student_search, name='student_search'),
     






    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance,
         name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave,
         name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification,
         name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,
         name='student_view_result'),

     path('student/results/preview/', student_views.student_view_result_preview,
          name='student_view_result_preview'),
     path('student/results/term_wise_list/', student_views.term_wise_list,
          name='term_wise_list'),
     path('student/results/get_terms/', student_views.get_terms,
          name='get_terms'),
     path('student/results/detailed_evaluation/', student_views.detailed_evaluation,
         name='detailed_evaluation'),
        
      path('student/results/get_term_wise_data', student_views.get_term_wise_data,
         name='get_term_wise_data'),
     path('student/results/generate_term_pdf/<str:term_wise>/', student_views.generate_term_pdf,
         name='generate_term_pdf'), 
     path('student/curriculam/student_view_curriculam/', student_views.student_view_curriculam,
         name='student_view_curriculam'),
     path("student/edit_student_leave/<int:leave_id>", student_views.edit_student_leave,
         name='edit_student_leave'),
     path("student/delete_student_leave/<int:leave_id>", student_views.delete_student_leave,
         name='delete_student_leave'),
     path("student/result/student_hpcard", student_views.student_hpcard,
         name='student_hpcard'),
     path("student/student_report_hpc/",student_views.student_report_hpc, name='student_report_hpc'),

     path('audit_log/', views.auditlog_view, name='auditlog_view'),

    #  Alumni Home Pages
    path('alumni/home/', views.alumni_home, name='alumni_home'),
#     path('alumni/home/', views.alumni_home, name='alumnis_home'),



     path('alumni/alumnis_home/',alumni_views.alumnis_home, name='alumnis_home'),
     path('alumni/view/profile/', alumni_views.alumni_student_view_profile, name='alumni_student_view_profile'),
     path('alumni/placement_cell/', alumni_views.placement_cell, name='placement_cell'),
     path('alumni/events/', alumni_views.view_events, name='view_events'),
     path('alumni/career_guidance/', alumni_views.view_careerguidance, name='view_careerguidance'),
     path('alumni/career_guidance/', alumni_views.view_careerguidance, name='view_careerguidance'),
    path('alumni/feedback/', alumni_views.alumni_feedback, name='alumni_feedback'),
    path('alumni/alumni_list/', alumni_views.alumni_list, name='alumni_list'),
    path('alumni/alumni_password/', alumni_views.alumni_password, name='alumni_password'),

    # Other URL patterns
    path('import/', hod_views.import_from_excel, name='import_from_excel'),
    re_path(r'^media/(?P<path>.*\.(mp4|m4v|webm|mov))$', serve_video),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
