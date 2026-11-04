import json
import requests
import logging
import random
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from auditlog.models import LogEntry
from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
# Create your views here.
from .models import Alumnimembers, CustomUser, Parent, Student
# from .models import  AlumniAdmin
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('django')

def signup(request, **kwargs):

    """
    Complete registration with name, address, user_type, and OTP.
    Flow:
    - POST with email, first_name, last_name, street_address, user_type
    - If user exists: return error
    - If user does not exist: create new CustomUser, generate OTP, send email
    - Return JSON response for AJAX
    """

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        street_address = request.POST.get('street_address', '').strip()
        city = request.POST.get('city', '').strip()
        district_name = request.POST.get('district_name', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', '').strip()
        user_type = request.POST.get('user_type', '').strip()
        period_of_study = request.POST.get('period_of_study', '').strip()

        # Validate required fields
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)
        if not first_name:
            return JsonResponse({'status': 'error', 'message': 'First name is required.'}, status=400)
        if not user_type:
            return JsonResponse({'status': 'error', 'message': 'User type is required.'}, status=400)
        if user_type == '8':
            try:
                period_of_study = str(int(period_of_study))
            except (TypeError, ValueError):
                return JsonResponse({'status': 'error', 'message': 'Year of passing is required.'}, status=400)
            if not 2000 <= int(period_of_study) <= 2041:
                return JsonResponse({'status': 'error', 'message': 'Year of passing must be between 2000 and 2041.'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
            # User exists: return error message
            return JsonResponse({'status': 'error', 'message': 'This account is already registered. Please log in or use a different email.'})
        except CustomUser.DoesNotExist:
            # New user: create and set otp as password
            otp_password = str(random.randint(100000, 999999))
            try:
                user = CustomUser.objects.create_user(
                    email=email, 
                    password=otp_password, 
                    first_name=first_name,
                    last_name=last_name or '',
                    user_type=user_type,
                    street_address=street_address or '',
                    city=city or '',
                    district_name=district_name or '',
                    state=state or '',
                    country=country or ''
                )
                user.otp = otp_password
                user.otp_created_at = timezone.now()
                user.set_password(otp_password)
                user.save(update_fields=['otp', 'password', 'otp_created_at', 'street_address', 'city', 'district_name', 'state', 'country', 'user_type'])
                print(user)
                if user_type == '8':
                    alumni, _ = Alumnimembers.objects.get_or_create(admin=user)
                    alumni.period_of_study = period_of_study
                    alumni.save(update_fields=['period_of_study'])
                try:
                    subject = 'Welcome to iMentor - OTP for Login'
                    message = f'Dear {user.first_name},\n\nYour account has been created successfully. Your OTP for login is: {otp_password}\n\nUse this OTP to sign in to your account.'
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, message, from_email, [user.email], fail_silently=False)
                except Exception as e:
                    logger = logging.getLogger(__name__)
                    logger.exception('Error sending email while creating user')
                    return JsonResponse({'status': 'warning', 'message': 'Account created but email failed to deliver.'})
                # If this user is a Parent (user_type '6'), link/update Parent record
                if str(user.user_type) == '6' or user.user_type == 6:
                    try:
                        parent_obj, _ = Parent.objects.get_or_create(admin=user)
                        # optional fields from signup form
                        student_id = request.POST.get('student_id') or request.POST.get('student')
                        if student_id:
                            try:
                                student = Student.objects.get(id=student_id)
                                parent_obj.student = student
                            except Student.DoesNotExist:
                                pass
                        joining_date = request.POST.get('joining_date')
                        if joining_date:
                            from datetime import datetime
                            try:
                                parent_obj.joining_date = datetime.strptime(joining_date, '%Y-%m-%d').date()
                            except Exception:
                                pass
                        siblings = request.POST.get('siblings')
                        if siblings:
                            try:
                                parent_obj.siblings = int(siblings)
                            except Exception:
                                pass
                        parent_obj.save()
                    except Exception:
                        logger.exception('Failed to create/update Parent record')

                return JsonResponse({'status': 'success', 'message': 'Account created and OTP sent to your email.', 'email': email})
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception('Error creating user')
                return JsonResponse({'status': 'error', 'message': 'Could not create user.'}, status=500)
    # For GET fallback, render a signup page with a form
    return render(request, 'main_app/signup.html')


def verify_otp(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
    email = request.POST.get('email') or request.POST.get('log_email')
    otp = request.POST.get('otp')
    if not email or not otp:
        return JsonResponse({'status': 'error', 'message': 'Both email and OTP are required.'}, status=400)
    logger.info('verify_otp attempt for email: %s', email)
    try:
        user = CustomUser.objects.get(email=email)
        # Check OTP expiry: default 10 minutes
        otp_expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        if user.otp_created_at:
            time_elapsed = timezone.now() - user.otp_created_at
            if time_elapsed.total_seconds() > otp_expiry_minutes * 60:
                return JsonResponse({'status': 'error', 'message': 'OTP has expired.'}, status=400)
        if user.otp and str(user.otp) == str(otp):
            # authenticate and login
            user = EmailBackend.authenticate(request, username=email, password=otp)
            if user is not None:
                login(request, user)
                # Return user type information for client-side redirection
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Login successful.',
                    'user_type': user.user_type
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Authentication failed.'}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'}, status=400)
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)



# ------------------- LOGIN VIEWS ------------------- #

def login_page(request):
    """If user already logged in, redirect to correct dashboard."""
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        elif request.user.user_type == '3':
            return redirect(reverse("student_home"))
        elif request.user.user_type == '4':
            return redirect(reverse("acc_admin_home"))
        elif request.user.user_type == '5':
            return redirect(reverse("dashboard_home"))
        elif request.user.user_type == '6':
            return redirect(reverse("parent_home"))
        elif request.user.user_type == '7':
            return redirect(reverse("alumniadmin_home"))
        elif request.user.user_type == '8':
            return redirect(reverse("alumnis_home"))
        else:
            return redirect(reverse("acc_admin_home"))
    return render(request, 'main_app/login.html')


def doLogin(request, **kwargs):
    """Handle POST login request (email + password)."""
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")

    email = request.POST.get('email')
    password = request.POST.get('password')

    # Authenticate using custom EmailBackend
    user = EmailBackend.authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return _redirect_user_by_type(user)
    else:
        messages.error(request, "Invalid email or password.")
        return redirect("/")


def _redirect_user_by_type(user):
    """Redirect user based on user_type."""
    if user.user_type == '1':
        return redirect(reverse("admin_home"))
    elif user.user_type == '2':
        return redirect(reverse("staff_home"))
    elif user.user_type == '3':
        return redirect(reverse("student_home"))
    elif user.user_type == '4':  # Academic Admin
        return redirect(reverse("acc_admin_home"))
    elif user.user_type == '5':  # Dashboard user (custom)
        return redirect(reverse("dashboard_home"))
    elif user.user_type == '6':  # Parent user (custom)
        return redirect(reverse("parent_home"))
    elif user.user_type == '7':  # Alumni Admin user (custom)
        return redirect(reverse("alumniadmin_home"))
    elif user.user_type == '8':  # Alumni Member
        return redirect(reverse("alumnis_home"))
    else:
        return redirect(reverse("login_page"))  # unknown type fallback


def dashboard_login(request):
    """Separate login for dashboard-only users (user_type=5)."""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        # ✅ Allow only non-superusers with user_type=5
        if user and not user.is_superuser and str(user.user_type) == '5':
            login(request, user)
            return redirect(reverse("dashboard_home"))

        messages.error(request, "Invalid dashboard credentials.")
        return redirect(reverse("main_app/login.html"))  # safer with reverse()

    # ✅ Use a separate template for dashboard login
    return render(request, "main_app/login.html")

def logout_user(request):
    """Logout any user (including superuser)."""
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login_page'))



# ------------------- AUDIT LOG ------------------- #

def auditlog_view(request):
    logs = LogEntry.objects.all().order_by('-timestamp')
    return render(request, 'audit_log/audit_log_view.html', {'logs': logs})


def test_view(request):
    logger.info("Test view was accessed.")
    return HttpResponse("Check the log file!")


# ------------------- ATTENDANCE ------------------- #

@csrf_exempt
def get_attendance(request):
    """Fetch attendance by subject and session."""
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')

    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)

        attendance_list = [
            {
                "id": attd.id,
                "attendance_date": str(attd.date),
                "session": attd.session.id,
            }
            for attd in attendance
        ]
        return JsonResponse(attendance_list, safe=False)
    except Exception as e:
        logger.error(f"Error fetching attendance: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)


# ------------------- FIREBASE CONFIG ------------------- #

def showFirebaseJS(request):
    """Firebase service worker for push notifications."""
    data = """
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
    importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

    firebase.initializeApp({
        apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
        authDomain: "sms-with-django.firebaseapp.com",
        databaseURL: "https://sms-with-django.firebaseio.com",
        projectId: "sms-with-django",
        storageBucket: "sms-with-django.appspot.com",
        messagingSenderId: "945324593139",
        appId: "1:945324593139:web:03fa99a8854bbd38420c86",
        measurementId: "G-2F2RXTL9GT"
    });

    const messaging = firebase.messaging();
    messaging.setBackgroundMessageHandler(function (payload) {
        const notification = JSON.parse(payload);
        const notificationOption = {
            body: notification.body,
            icon: notification.icon
        }
        return self.registration.showNotification(payload.notification.title, notificationOption);
    });
    """
    return HttpResponse(data, content_type='application/javascript')


# ------------------- PARENT & ALUMNI HOME VIEWS ------------------- #



@login_required(login_url='login_page')
def alumni_home(request):
    """
    Alumni home page dashboard.
    """
    if request.user.user_type != '8':
        return redirect('login_page')
    
    from . import alumni_views
    return alumni_views.alumnis_home(request)











