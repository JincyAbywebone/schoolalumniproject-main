from dataclasses import fields
from typing import Any
from django import forms
from django.forms.widgets import DateInput, TextInput
from django.core.validators import RegexValidator
from datetime import date
from .models import *
from collections import OrderedDict

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=[('s', 'Select'),('M', 'Male'), ('F', 'Female'), ('O', 'Others')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    city = forms.CharField(required=False)
    district_name =forms.CharField(required=False)
    country = forms.CharField(required=False)
    state = forms.CharField(required=False)
    street_address = forms.CharField(required=False)
    date_of_birth=forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'forms-control','type':"date"}))
   # religion=forms.forms.CharField()

    widget = {
        'password': forms.PasswordInput(),
    }

    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            if isinstance(instance, CustomUser):
                user = instance
            else:
                user = getattr(instance, 'admin', None) or getattr(instance, 'alumniadmin', None)

            if user is None:
                return

            instance = user.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            instance = self.instance
            if isinstance(instance, CustomUser):
                user = instance
            else:
                user = getattr(instance, 'admin', None) or getattr(instance, 'alumniadmin', None)
            dbEmail = user.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'gender',  'street_address' , 'city', 'district_name', 'state', 'country', 'profile_pic',  'date_of_birth' ]


class StudentForm(CustomUserForm):
    admission_number = forms.CharField(required=False)
    parent_name = forms.CharField(required=False)
    guardian_contact_number = forms.CharField(required=False)
    mother_tongue = forms.CharField(required=False)
    mother_name = forms.CharField(required=False)
    blood_group = forms.CharField(required=False) 
    caste = forms.CharField(required=False) 
    religion = forms.CharField(required=False)
    aadhar_number = forms.CharField(required=False)
    school_house = forms.CharField(required=False)
    bus_stop = forms.CharField(required=False)
    bus_number = forms.CharField(required=False)
    allergies_medical_conditions = forms.CharField(required=False)
    alternate_contact_number = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)


    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
            ['course', 'session', 'admission_number', 'parent_name', 'guardian_contact_number','mother_name','blood_group','mother_tongue','caste','religion','aadhar_number','school_house','bus_stop','bus_number','allergies_medical_conditions','alternate_contact_number']

          
class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class AccAdminForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep current password'}),
        label="New Password"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'gender', 'profile_pic',
            'street_address', 'city', 'district_name', 'state', 'country',
            'date_of_birth', 'new_password'
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district_name': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'new_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AccAdminForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AlumniAdminForm(CustomUserForm):
    year_of_passing = forms.TypedChoiceField(
        choices=[('', 'Select year')] + [(year, str(year)) for year in range(2000, 2041)],
        required=False,
        empty_value=None,
        coerce=int,
    )

    def __init__(self, *args, **kwargs):
        super(AlumniAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['year_of_passing'].initial = self.instance.year_of_passing

    def clean_email(self):
        return super().clean_email()

    class Meta(CustomUserForm.Meta):
        model = AlumniAdmin
        fields = CustomUserForm.Meta.fields + ['year_of_passing']


class AlumnimembersForm(CustomUserForm):
    mobile = forms.CharField(required=False, max_length=10)
    period_of_study = forms.TypedChoiceField(
        choices=[('', 'Select year')] + [(year, str(year)) for year in range(2000, 2042)],
        required=False,
        coerce=str,
    )
    employment_status = forms.CharField(required=False)
    employment_remarks = forms.CharField(required=False, widget=forms.Textarea)
    employment_sectors = forms.CharField(required=False)
    current_street_address = forms.CharField(required=False)
    current_city = forms.CharField(required=False)
    current_district_name = forms.CharField(required=False)
    current_state = forms.CharField(required=False)
    course_studied = forms.CharField(required=False)
    on_campus_achievements = forms.CharField(required=False, widget=forms.Textarea)
    beyond_college_achievements = forms.CharField(required=False, widget=forms.Textarea)
    outside_institution_course = forms.CharField(required=False, widget=forms.Textarea)
    contribution = forms.CharField(required=False, widget=forms.Textarea)
    mode_of_payment = forms.CharField(required=False)
    membershipfees = forms.CharField(required=False)
    willingness = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    same_as_permanent = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(AlumnimembersForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Alumnimembers
        fields = CustomUserForm.Meta.fields + [
            'mobile', 'period_of_study', 'employment_status', 'employment_remarks', 'employment_sectors',
            'current_street_address', 'current_city', 'current_district_name', 'current_state',
            'course_studied', 'on_campus_achievements', 'beyond_college_achievements', 'outside_institution_course',
            'contribution', 'mode_of_payment', 'membershipfees', 'willingness', 'is_active', 'course', 'department'
        ]
class ChatGroupForm(forms.ModelForm):
    period_of_study = forms.ChoiceField(choices=[])

    class Meta:
        model = ChatGroup
        fields = ['course', 'period_of_study']

    def __init__(self, *args, **kwargs):
        super(ChatGroupForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()

        # Get distinct non-null period_of_study values
        periods = Alumnimembers.objects.exclude(
            models.Q(period_of_study__isnull=True) | models.Q(period_of_study__exact='')
        ).values_list('period_of_study', flat=True).distinct()

        period_choices = [(p, p) for p in periods]
        self.fields['period_of_study'].choices = period_choices
        
class AddMemberForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    period_of_study = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only include non-null periods
        periods = Alumnimembers.objects.exclude(
            models.Q(period_of_study__isnull=True) | models.Q(period_of_study__exact='')
        ).values_list('period_of_study', flat=True).distinct()
        self.fields['period_of_study'].choices = [(p, p) for p in periods]


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields +  \
           ['department','course','contact_number']


class ParentForm(CustomUserForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, label="Course", empty_label="Select Course")
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        label="Students",
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 8})
    )
    joining_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    siblings = forms.IntegerField(required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Parent
        fields = CustomUserForm.Meta.fields + ['course', 'students', 'joining_date', 'siblings']


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name', 'division']
        model = Course

class CurriculamForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CurriculamForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Curriculam
        # fields = ['course','subject','staff','lesson']
        fields = ['title','lesson']

class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['subject','staff','course']   

class SchoolForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = School
        fields = ['name', 'address', 'city', 'state', 'country', 'phone', 'email', 'image']

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DepartmentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)        

    class Meta:
        model = Department
        fields = ['name']

class SubjectmasterForm(FormSettings):
   def __init__(self, *args, **kwargs):
        super(SubjectmasterForm, self).__init__(*args, **kwargs)
   class Meta:
        model = Subjectmaster
        fields = ['name','department'] 

class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message','image']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message','image']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class AlumniFeedbackForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AlumniFeedbackForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AlumniFeedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your feedback here...'})
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']



class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields +  \
                  ['course', 'session', 'admission_number', 'parent_name', 'mother_tongue']


class StaffEditForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep current password'}),
        label="New Password"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'gender', 'profile_pic',
            'street_address', 'city', 'district_name', 'state', 'country',
            'date_of_birth'
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district_name': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in self.Meta.widgets:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class AdminEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields

class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)
    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['student', 'test', 'remarks', 'term']
        #  fields = ['session_year', 'subjectmaster', 'student', 'test', 'exam', 'remarks','term']
class FeeSettingsForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(FeeSettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeeSettings
        fields = ['fee_name','fee_type']

class ExcelUploadForm(forms.Form):
    file = forms.FileField()  

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Select Excel File')   

class AluminiExcelForm(forms.Form):
    excel_form = forms.FileField(label='Select Excel File')   

class AlumniMembersForm(CustomUserForm):
    period_of_study = forms.TypedChoiceField(
        choices=[('', 'Select year')] + [(year, str(year)) for year in range(2000, 2042)],
        required=False,
        coerce=str,
        label='Period of Study',
    )

    def __init__(self, *args, **kwargs):
        # Allow passing the current request/user for permission checks
        self.request_user = kwargs.pop('user', None)
        super(AlumniMembersForm, self).__init__(*args, **kwargs)

        # Populate start/end year choices (descending from current year to 1950)
        # current_year = date.today().year
        # years = [(str(y), str(y)) for y in range(current_year, 1949, -1)]
        # self.fields['start_year'].choices = [('', '-----')] + years
        # self.fields['end_year'].choices = [('', '-----')] + years
        
        # If editing an instance, split the existing period_of_study to populate selects
        # if kwargs.get('instance'):
        #     instance = kwargs.get('instance')
        #     period = getattr(instance, 'period_of_study', None)
        #     if period:
        #         try:
        #             s,e = period.split('-')
        #             self.fields['start_year'].initial = s
        #             self.fields['end_year'].initial = e
        #         except Exception:
        #             pass

        # Hide 'is_active' for normal users (self-registration)
        if self.request_user and not (self.request_user.is_staff or str(self.request_user.user_type) in ['1','2','4','6']):
            if 'is_active' in self.fields:
                del self.fields['is_active']

    mobile = forms.CharField(max_length=10,validators=[RegexValidator(r'^\d{10}$', message="Mobile number must be exactly 10 digits.")])
    same_as_permanent = forms.BooleanField(required=False, label="Same as Permanent Address")

    # Split the period of study into two selects in the form for better UX
    #    start_year = forms.ChoiceField(choices=[], required=False, label="Start Year", widget=forms.Select(attrs={'class':'form-control'}))
    #    end_year = forms.ChoiceField(choices=[], required=False, label="End Year", widget=forms.Select(attrs={'class':'form-control'}))


    class Meta(CustomUserForm.Meta):
        same_as_permanent = forms.BooleanField(required=False, label="Same as Permanent Address")
        model = Alumnimembers
        fields = CustomUserForm.Meta.fields[:4] + ['blood_group'] + CustomUserForm.Meta.fields[4:] + \
           ['same_as_permanent','current_street_address','current_city','current_district_name','current_state','course','department','mobile','period_of_study','employment_status','employment_remarks','employment_sectors','course_studied','on_campus_achievements','beyond_college_achievements','outside_institution_course','contribution','mode_of_payment','membershipfees','willingness','is_active' ]

        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
            'permanent_locality': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_district': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_state': forms.TextInput(attrs={'class': 'form-control'}),
            'current_locality': forms.TextInput(attrs={'class': 'form-control'}),
            'current_district': forms.TextInput(attrs={'class': 'form-control'}),
            'current_state': forms.TextInput(attrs={'class': 'form-control'}),
            # Keep the model field but hide the raw input; we use two selects (`start_year`, `end_year`) instead
            #'period_of_study': forms.HiddenInput(),
            'period_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_of_payment': forms.TextInput(attrs={'class': 'form-control'})
       }

        labels = {
            'mode_of_payment': "Mode of Payment"
        }

        help_texts = {
            'mode_of_payment': (
                "Details of membership fee paid (Rs 100/-)\n"
                "If cash – receipt no; If Cheque – Cheque no; If online – UPI transaction ID/ Date/ Time\n"
                "To pay:\n"
                "UPI ID: alumnistxvkm@sbi\n"
                "Account No: 43289388016\n"
                "Bank and Branch: SBI Ullala IFSC: SBIN0008682"
            )
        

        

        }


class FeeAmountSettingsForm(FormSettings):
    def _init_(self, *args, **kwargs):
        super(FeeAmountSettingsForm, self)._init_(*args, **kwargs)

    class Meta:
        model = FeeAmountSettings
        fields = ['fee_name', 'fee_type', 'amount', 'course', 'session']


class StaffAttendanceForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(StaffAttendanceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StaffAttendance
        fields = ['date','staff','fn','an']


class LessonSettingsForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LessonSettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LessonSettings
        fields = ['date','notes','image']
        widgets = {
            'date':  DateInput(attrs={'type': 'date'}),
             
        }

class ExamtypeSettingsForm(FormSettings):
    exam_type = forms.ChoiceField(choices=[('Select', 'Select'),('Periodic Test', 'Periodic Test'), ('Test Paper', 'Test Paper'), ('Semester', 'Semester')], widget=forms.Select(attrs={'class': 'form-control'}))
    exam_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    term = forms.ChoiceField(choices=[('Term-1', 'Term-1'), ('Term-2', 'Term-2')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    max_marks = forms.FloatField(required=True, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    exam_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super(ExamtypeSettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExamtypeSettings
        fields = ['exam_type', 'exam_name', 'term', 'max_marks','exam_date']
        widgets = {
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'term': forms.TextInput(attrs={'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
class AlumniEventsForm(forms.ModelForm):
    image = forms.ImageField()
    event_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class':'forms-control','type':"date"}))
    class Meta:
        model = AlumniEventsInfo
        fields = ['event_name', 'event_date', 'event_type','event_venue','event_status','course','description', 'image']

    def __init__(self, *args, **kwargs):
        super(AlumniEventsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class JobPostingForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = CareerInfo
        fields = ['designation', 'employer', 'location', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(JobPostingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if 'image' in self.fields:
            self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class CareerGuidanceForm(forms.ModelForm):
    image = forms.ImageField()
    programme_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class':'forms-control','type':"date"}))
    class Meta:
        model = CareerGuidance
        fields = ['programme_name', 'programme_date', 'programme_type','programme_venue','programme_status','course','description', 'image']

    def __init__(self, *args, **kwargs):
        super(CareerGuidanceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'    

class ModuleSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModuleSettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ModuleSettings
        fields = ['school','module','status']                    


# ===================== LMS Forms =====================

class LMSVideoForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LMSVideoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LMSVideo
        fields = ['title', 'description', 'video']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class LMSImageForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LMSImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LMSImage
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class LMSNoteForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LMSNoteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LMSNote
        fields = ['title', 'content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class AssociatedCompaniesForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = AssociatedCompanies
        fields = ['company_name', 'website', 'contact', 'company_overview', 'image']

    def __init__(self, *args, **kwargs):
        super(AssociatedCompaniesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if 'image' in self.fields:
            self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

class AlumniProfileEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep current password'}),
        label="New Password"
    )

    BLOOD_GROUP_CHOICES = [
        ('', 'Select Blood Group'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES, 
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'gender', 'blood_group', 'profile_pic',
            'street_address', 'city', 'district_name', 'state', 'country',
            'date_of_birth',
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district_name': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AlumniProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class AddSettingsForm(forms.Form):
     course = forms.ModelChoiceField(queryset=Course.objects.all())
    period_of_study = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only include non-null periods
        periods = Alumnimembers.objects.exclude(
            models.Q(period_of_study__isnull=True) | models.Q(period_of_study__exact='')
        ).values_list('period_of_study', flat=True).distinct()
        self.fields['period_of_study'].choices = [(p, p) for p in periods]       
