from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user?

        # ✅ Allow unauthenticated users to access these URLs
        allowed_paths = [
            reverse('login_page'),
            reverse('user_logout'),
            reverse('dashboard_login'),
            reverse('user_login'),
            reverse('signup'),
            reverse('verify_otp'),
            # reverse('dashboard_logout'),
        ]

        # Allow Django's own auth views (password reset, etc.) and static/media files
        if modulename in ['django.contrib.auth.views', 'django.views.static'] or request.path in allowed_paths or request.path.startswith('/media/') or request.path.startswith('/static/'):
            return None

        # ✅ If user not logged in — redirect to login
        if not user.is_authenticated:
            return redirect(reverse('login_page'))

        # ✅ If logged in, redirect based on role
        if user.user_type == '1':  # Admin/HOD
            if modulename == 'main_app.student_views':
                return redirect(reverse('admin_home'))

        elif user.user_type == '2':  # Staff
            if modulename in ['main_app.student_views', 'main_app.hod_views']:
                return redirect(reverse('staff_home'))

        elif user.user_type == '3':  # Student
            if modulename in ['main_app.hod_views', 'main_app.staff_views']:
                return redirect(reverse('student_home'))

        elif user.user_type == '4':  # Academic Admin
            if modulename in ['main_app.student_views', 'main_app.hod_views']:
                return redirect(reverse('acc_admin_home'))

        elif user.user_type == '5':  # Dashboard user (custom)
            # Restrict access to dashboard modules only
            if modulename not in ['main_app.super_views', 'main_app.acc_admin_views']:
                return redirect(reverse('dashboard_home'))
        elif user.user_type == '6':  # Parent
            # Restrict access to parent modules only
            if modulename not in ['main_app.parent_views', 'main_app.hod_views']:
                return redirect(reverse('parent_home'))
        elif user.user_type == '7':
                if modulename not in ['main_app.alumniadmin_views']:
                    return redirect(reverse('alumniadmin_home'))    

        elif user.user_type == '8':  # Alumni Member
            # Restrict access to alumni views only (alumni views live in main_app.views)
            if modulename not in ['main_app.alumni_views']:
                return redirect(reverse('alumnis_home'))    

        # ✅ No redirect if user accessing valid area
        return None

    def process_response(self, request, response):
        if request.path.startswith('/media/'):
            response['Cache-Control'] = 'no-cache, must-revalidate'
        return response
