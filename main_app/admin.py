from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
#from import_export.admin import ImportExportModelAdmin # type: ignore


# Register your models here.
#class userdata(ImportExportModelAdmin):
# pass

class UserModel(UserAdmin):
    ordering = ('email',)


class ParentAdmin(admin.ModelAdmin):
    """Admin for Parent model with ManyToMany students display."""
    list_display = ('id', 'parent_name', 'joining_date', 'siblings', 'students_list')
    list_filter = ('joining_date',)
    search_fields = ('admin__first_name', 'admin__last_name', 'admin__email')
    filter_horizontal = ('students',)  # Makes ManyToMany easier to manage
    readonly_fields = ('students_list',)
    
    def parent_name(self, obj):
        """Display parent's full name."""
        try:
            return f"{obj.admin.first_name} {obj.admin.last_name}"
        except:
            return "N/A"
    parent_name.short_description = "Parent Name"
    
    def students_list(self, obj):
        """Display linked students as comma-separated list."""
        students = obj.students.all()
        if students:
            return ", ".join([
                f"{s.admin.first_name} {s.admin.last_name} ({s.admission_number})" 
                for s in students
            ])
        return "No students linked"
    students_list.short_description = "Linked Students"


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(Parent, ParentAdmin)
