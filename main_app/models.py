from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from auditlog.registry import auditlog
from django.utils import timezone
# from .models import ModuleSetting
# from .models import Student, staff, Course, CustomUser, Subjectmaster, Subject, Department, Session, File, School, Attendance, ExamtypeSettings, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedbackStudent, FeedbackStaff, NotificationStaff, NotificationStudent, StudentResult, Curriculam, FeeSettings, FeeAmountSettings, LessonSettings, AlumniMembers, StaffAttendance, StudentPromotion

class File(models.Model):
    file = models.FileField(upload_to="excel")

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)

    def create_dashboard_user(self):
        """Create a hardcoded dashboard user (not superuser)."""
        email = "dashboard@myapp.com"
        password = "Dashboard@123"
        extra_fields = {
            "is_staff": True,
            "is_superuser": True,
            "user_type": "5",
        }

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            user = self._create_user(email, password, **extra_fields)
        return user
 #--------------------------------------------------------------       

class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4, "Academic Admin"),(5, "Super Admin"), (6, "Parent"),(7, "Alumni Admin"), (8, "Alumni Member"))
    GENDER = [("M", "Male"), ("F", "Female"), ("O", "Others")]


    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(null=True, blank=True)
    city = models.TextField(default="")
    state = models.TextField(default="")
    street_address = models.TextField(default="")
    district_name = models.TextField(default="")
    country = models.TextField(default="")
    date_of_birth=models.DateField(null=True,  blank=True)
    # blood_group = models.CharField(max_length=10, null=True, blank=True)
    fcm_token = models.TextField(default="")  # For firebase notifications
    otp = models.CharField(max_length=6, null=True, blank=True)  # OTP field
    otp_created_at = models.DateTimeField(null=True, blank=True)  # OTP creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        super(CustomUser, self).save(*args, **kwargs)
    def __str__(self):
        return self.first_name + ", " + self.last_name

    @property
    def profile_pic_url(self):
        if not self.profile_pic:
            return ""
        try:
            url = self.profile_pic.url
            if url.startswith('/media/media/'):
                return url.replace('/media/media/', '/media/', 1)
            return url
        except Exception:
            name = str(self.profile_pic.name if hasattr(self.profile_pic, 'name') else self.profile_pic)
            if not name:
                return ""
            clean = name.replace('\\', '/').lstrip('/')
            if clean.startswith('media/'):
                return '/' + clean
            return f"/media/{clean}"

class Department(models.Model):
    # staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
  
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Department, self).save(*args, **kwargs)
       
    def __str__(self):
        return self.name    


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class AccAdmin(models.Model):
    accadmin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=120)
    division = models.CharField(max_length=120,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.division = self.division.upper()
        super(Course, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} - {self.division}"

class Student(models.Model):
    STATUS_CHOICES = (
    ("ACTIVE", "Active"),
    ("TRANSFERRED", "Transferred"),
    ("PASSEDOUT", "Passed Out"),
    )
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    admission_number = models.TextField(null=True, blank=True, default="")
    parent_name = models.TextField()
    parents = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True, related_name='student_list')
    guardian_contact_number = models.CharField(max_length=10,default="")
    mother_name = models.TextField(default="")
    blood_group = models.TextField(default="")
    mother_tongue = models.TextField()
    caste = models.TextField(null=True, blank=True, default="")
    religion = models.TextField(null=True, blank=True, default="")
    aadhar_number = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{12}$', message="Aadhar number must be exactly 12 digits.")], default="")
    school_house = models.CharField(max_length=120, default="")
    bus_stop = models.CharField(max_length=120, default="")
    bus_number = models.CharField(max_length=120, default="")
    allergies_medical_conditions = models.TextField(default="")
    alternate_contact_number = models.CharField(max_length=10, default="")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="ACTIVE")
    admission_date = models.DateField(null=True,blank=True)
    file_type = models.TextField(default="")

    def __str__(self):
        return self.admin.first_name + ", " + self.admin.last_name
    class Meta:
        db_table = 'main_app_student'

class TransferCertificate(models.Model):
    student = models.ForeignKey(Student,on_delete=models.PROTECT,related_name="transfer_certificates")
    tc_number = models.CharField(max_length=30,unique=True)
    issue_date = models.DateField(default=timezone.now)
    leaving_date = models.DateField()
    last_attended_date = models.DateField(null=True,blank=True)
    CONDUCT_CHOICES = (("Excellent", "Excellent"),("Very Good", "Very Good"),("Good", "Good"),("Satisfactory", "Satisfactory"),)
    conduct = models.CharField(max_length=50,choices=CONDUCT_CHOICES,default="Good")
    qualified_for_promotion = models.BooleanField(default=True)
    REASON_CHOICES = (("TRANSFER", "Transfer to another school"),("PASSED_OUT", "Passed Out"),("PARENT_TRANSFER", "Parent Transfer"),("ABROAD", "Going Abroad"),
("DISCONTINUED", "Discontinued"),("OTHER", "Other"),)
    reason = models.CharField(max_length=30,choices=REASON_CHOICES,default="OTHER")

    reason_description = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    issued_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name="issued_transfer_certificates")
    cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):

        if not self.tc_number:

            year = timezone.now().year

            last = TransferCertificate.objects.filter(
                tc_number__startswith=f"TC/{year}/"
            ).order_by("-id").first()

            if last:

                try:
                    number = int(last.tc_number.split("/")[-1]) + 1
                except (ValueError, IndexError):
                    number = 1
            else:

                number = 1

            self.tc_number = f"TC/{year}/{number:04d}"

        super().save(*args, **kwargs)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.tc_number

class AlumniAdmin(models.Model):
    alumniadmin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    year_of_passing = models.IntegerField(
        choices=[(year, str(year)) for year in range(2000, 2041)],
        null=True,
        blank=True,
    )


class Alumnimembers(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=True)
    mobile = models.CharField(max_length=10, default="", blank=True)
    period_of_study = models.CharField(max_length=120, default="", blank=True)
    employment_status = models.CharField(max_length=120, default="", blank=True)
    employment_remarks = models.TextField(default="", blank=True)
    employment_sectors = models.CharField(max_length=200, default="", blank=True)
    current_street_address = models.CharField(max_length=255, default="", blank=True)
    current_city = models.CharField(max_length=120, default="", blank=True)
    current_district_name = models.CharField(max_length=120, default="", blank=True)
    current_state = models.CharField(max_length=120, default="", blank=True)
    course_studied = models.CharField(max_length=150, default="", blank=True)
    on_campus_achievements = models.TextField(default="", blank=True)
    beyond_college_achievements = models.TextField(default="", blank=True)
    outside_institution_course = models.TextField(default="", blank=True)
    contribution = models.TextField(default="", blank=True)
    mode_of_payment = models.CharField(max_length=120, default="", blank=True)
    membershipfees = models.CharField(max_length=120, default="", blank=True)
    willingness = models.CharField(max_length=120, default="", blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


class Staff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10,default="")
    permission = models.BooleanField(default=False)
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Parent(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    siblings = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        try:
            return f"Parent: {self.admin.first_name} {self.admin.last_name}"
        except Exception:
            return "Parent"


class ParentAdminNotification(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='admin_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='verification_requests',null=True,      # ADD THIS
    blank=True      # ADD THIS
)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Pending')
    def __str__(self):
        return f"Notification for {self.parent.admin.first_name} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class Subjectmaster(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Subjectmaster, self).save(*args, **kwargs)
    def __str__(self):
         return self.name
        

class Subject(models.Model):
    # name = models.CharField(max_length=120)
    subject = models.ForeignKey(Subjectmaster,on_delete=models.DO_NOTHING, null=True, blank=False)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class School(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)  # Increased max_length
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)  # Increased max_length for email
    image = models.ImageField(null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(School, self).save(*args, **kwargs)
    def __str__(self):
         return self.name

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExamtypeSettings(models.Model):
    exam_type = [("Periodic Test", "Periodic Test"), ("Test Paper", "Test Paper"), ("Semester", "Semester"),]
    exam_type = models.CharField(max_length=50,choices=exam_type,default="")
    exam_name = models.CharField(max_length=50)
    term = models.CharField(max_length=50) 
    max_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exam_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
      self.exam_name = self.exam_name.upper()  # ✅ This is fine only if self.name is a string
      super(ExamtypeSettings, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.exam_type}"


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image= models.ImageField(null=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image= models.ImageField(null=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    subjectmaster = models.ForeignKey(Subjectmaster,on_delete=models.DO_NOTHING, null=True, blank=False)
    test = models.CharField(max_length=5, default='0')      # Changed from FloatField
    exam = models.CharField(max_length=5, default='0')      # Changed from FloatField
    semester = models.CharField(max_length=5, default='0') 
    exam_type = models.ForeignKey(ExamtypeSettings, on_delete=models.CASCADE, null=True, blank=False)
    remarks = models.TextField(default=0)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True, blank=False)
    TERM_CHOICES = [
        ('Term-1', 'Term-1'),
        ('Term-2', 'Term-2'),
    ]
    # term = models.TextField(default=0)
    term = models.CharField(max_length=50,choices=TERM_CHOICES, default='Term-1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Curriculam(models.Model):
     title = models.CharField(max_length=120, null=True, blank=True)
     status = models.BooleanField(default=False)
     course = models.ForeignKey(Course, on_delete=models.DO_NOTHING,null=True, blank=False) 
    #  staff =  models.ForeignKey(Staff, on_delete=models.DO_NOTHING,null=True, blank=False)
     subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,null=True, blank=False) 
     lesson = models.TextField()
     term = models.TextField(max_length=120)
     notificaton = models.TextField(default=False)
    #  accadmin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
     def save(self,*args, **kwargs):
          self.lesson=self.lesson.upper()
          super(Curriculam, self).save(*args, **kwargs)
     def __str__(self):
        return f"{self.lesson} - {self.course} - {self.subject}"
     
class FeeSettings(models.Model):
     #academic_year = models.CharField(max_length=50, default=0)
     fee_name = models.CharField(max_length=50)
     fee_type = models.CharField(max_length=50)
     
     def save(self, *args, **kwargs):
        if not (self.fee_name or self.fee_type):
            raise ValidationError("At least one field must be filled before saving.")
        super().save(*args, **kwargs)


class ModuleSettings(models.Model):

     MODULE_CHOICES = [
        ('M1', 'Academic'),
        ('M2', 'Alumni'),
    ]
    #  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     school = models.ForeignKey(School, on_delete=models.CASCADE)
     module = models.CharField(max_length=10, choices=MODULE_CHOICES)
     status = models.BooleanField(default=False)
     date = models.DateTimeField(auto_now_add=True)
   


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)
        if instance.user_type == 4:
            AccAdmin.objects.create(accadmin=instance)
        if instance.user_type == 7:
            AlumniAdmin.objects.create(alumniadmin=instance)
        if str(instance.user_type) == '8' or instance.user_type == 8:
            Alumnimembers.objects.get_or_create(admin=instance)
        if str(instance.user_type) == '6' or instance.user_type == 6:
            Parent.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.accadmin.save() 
    if instance.user_type == "7" and hasattr(instance, 'alumniadmin'):
        instance.alumniadmin.save()
    if instance.user_type == "8" and hasattr(instance, 'alumnimembers'):
        instance.alumnimembers.save()


    if str(instance.user_type) == '6' or instance.user_type == 6:
        try:
            instance.parent.save()
        except Parent.DoesNotExist:
            # Parent instance might not yet exist; ignore and let creation handler run
            pass
        except Exception:
            # Avoid breaking save on unexpected errors
            pass

class Alumnimembers(models.Model):
    STATUS = [("Employed","Employed"),("Seeking Employment","Seeking Employment"),("Self Employed","Self Employed"),("Business","Business"),("Student","Student"),("Unemployed","Unemployed")]
    SECTORS = [("Agriculture","Agriculture"),("Construction","Construction"),("Education","Education"),("Finance","Finance"),("Fisheries","Fisheries"),("Healthcare","Healthcare"),("Information Technology","Information Technology"),("Maritime","Maritime"),("Oil and Gas","Oil and Gas"),("Public Sector","Public Sector"),("Private Sector","Private Sector"),("Transportation","Transportation"),("Tourism and Hospitality","Tourism and Hospitality"),("Others","Others")]
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    mobile = models.CharField(max_length=10,validators=[RegexValidator(r'^\d{10}$', message="Mobile number must be exactly 10 digits.")])
    current_street_address = models.CharField(max_length=130)
    current_city = models.CharField(max_length=130)
    current_district_name = models.CharField(max_length=130)
    current_state = models.CharField(max_length=150)
    period_of_study = models.CharField(max_length=150)
    employment_status = models.CharField(max_length=50,choices=STATUS,default="")
    employment_remarks = models.CharField(max_length=255,null=True)
    employment_sectors = models.CharField(max_length=100,choices=SECTORS,null=True)
    course_studied = models.CharField(max_length=150,null=True,blank=True)
    on_campus_achievements = models.CharField(max_length=255,null=True,blank=True)
    beyond_college_achievements = models.CharField(max_length=255,null=True,blank=True)
    outside_institution_course = models.CharField(max_length=255,null=True,blank=True)
    contribution = models.CharField(max_length=255,null=True,blank=True)
    mode_of_payment = models.CharField(max_length=255,null=True,blank=True)
    membershipfees = models.CharField(max_length=255,null=True,blank=True)
    willingness = models.CharField(max_length=150,null=True,blank=True)
    # Blood Group choices added for alumni profile
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     self.first_name = self.first_name.upper()
    #     super(Alumnimembers, self).save(*args, **kwargs)
    # def __str__(self):
    #      return self.first_name


class StaffAttendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    fn = models.BooleanField(default=False)
    an = models.BooleanField(default=False)
    date = models.DateField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        super(Alumnimembers, self).save(*args, **kwargs)
    def __str__(self):
         return self.first_name
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] 


class ChatGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default=True)
    period_of_study = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.period_of_study}"

class GroupMembership(models.Model):
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True) 
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name if self.user else 'Unknown User'} in {self.chat_group}"

class GroupChatMessage(models.Model):
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, related_name="sent_message", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.admin.first_name}: {self.message[:30]}"


    
class FeeAmountSettings(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING,null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING,null=True, blank=False)
    fee_name = models.CharField(max_length=50,default='Tuition Fee')
    fee_type = models.CharField(max_length=50)
    amount = models.FloatField(max_length=50,default=0)

class LessonSettings(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,null=True, blank=False)
    curriculam = models.ForeignKey(Curriculam, on_delete=models.DO_NOTHING,null=True, blank=False)
   # title = models.ForeignKey(Curriculam, on_delete=models.DO_NOTHING,null=True, blank=False)
    notes = models.TextField()
    image= models.ImageField(null=True)
    date = models.DateField(null=True)

    # def __str__(self):
    #     return f"{self.subject} - {self.curriculam}"

# ===================== LMS Models =====================

class LMSVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    video = models.FileField(upload_to="lms/videos/")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LMSImage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="lms/images/")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LMSNote(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="lms/notes/", null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# ======================================================

class AlumniEventsInfo(models.Model):
    STATUS = [("Scheduled","Scheduled"),("Postponed","Postponed"),("Cancelled","Cancelled")]
    event_name = models.CharField(max_length=150)
    event_date =  models.DateField()
    event_type = models.CharField(max_length=200)
    event_venue =  models.CharField(max_length=100)
    event_status = models.CharField(max_length=50,choices=STATUS,default="")
    description =  models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CareerGuidance(models.Model):
    STATUS = [("Scheduled","Scheduled"),("Postponed","Postponed"),("Cancelled","Cancelled"),("Conducted","Conducted")]
    programme_name = models.CharField(max_length=150)
    programme_date =  models.DateField()
    programme_type = models.CharField(max_length=200)
    programme_venue =  models.CharField(max_length=100)
    programme_status = models.CharField(max_length=50,choices=STATUS,default="")
    description =  models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CareerInfo(models.Model):
    designation = models.CharField(max_length=150)
    employer = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='jobpostings/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation} at {self.employer}"

class AssociatedCompanies(models.Model):
    company_name = models.CharField(max_length=150)
    website = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    company_overview = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='companies/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class AlumniFeedback(models.Model):
    alumni = models.ForeignKey("AlumniMembers", on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()  # Stores the admin's response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.alumni.admin.first_name} {self.alumni.admin.last_name}"

class CareerInfo(models.Model):
    designation = models.CharField(max_length=150)
    employer =  models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    description =  models.CharField(max_length=255, null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserLoginRecord(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.CustomUser.first_name}.{self.CustomUser.last_name} logged in at {self.login_time}"
    
class AuditableModel(models.Model):
    class Meta:
        abstract = True  # not a real table

    # optional: common fields

    def save(self, *args, **kwargs):
        # Custom logging hooks can go here
        super().save(*args, **kwargs)    

auditlog.register(Student)
auditlog.register(Staff)
auditlog.register(Course) 
auditlog.register(CustomUser)     
auditlog.register(Subjectmaster)  
auditlog.register(Subject)
auditlog.register(Department)
auditlog.register(Session)
auditlog.register(File)
auditlog.register(School)
auditlog.register(Attendance)
auditlog.register(ExamtypeSettings)
auditlog.register(AttendanceReport)
auditlog.register(LeaveReportStudent)
auditlog.register(LeaveReportStaff)
auditlog.register(FeedbackStudent)
auditlog.register(FeedbackStaff)
auditlog.register(NotificationStaff)
auditlog.register(NotificationStudent)
auditlog.register(StudentResult)
auditlog.register(Curriculam)
auditlog.register(FeeSettings)
auditlog.register(FeeAmountSettings)
auditlog.register(LessonSettings)
auditlog.register(CareerInfo)
auditlog.register(AssociatedCompanies)
auditlog.register(AlumniFeedback)
auditlog.register(Alumnimembers)


class StudentPromotion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='promotions_from')
    from_session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True, related_name='promotions_from')
    to_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='promotions_to')
    to_session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True, related_name='promotions_to')
    remarks = models.TextField(default="", blank=True)
    promoted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.admin.first_name} {self.student.admin.last_name} promoted from {self.from_course} to {self.to_course}"

auditlog.register(StudentPromotion)
auditlog.register(LMSVideo)
auditlog.register(LMSImage)
auditlog.register(LMSNote)
auditlog.register(CareerInfo)
auditlog.register(AlumniFeedback)
