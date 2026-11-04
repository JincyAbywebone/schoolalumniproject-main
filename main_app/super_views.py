import json
import requests
import openpyxl
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.shortcuts import render
from openpyxl import load_workbook
from .models import Student
from .forms import ModuleSettingsForm
from .models import CustomUser
from .forms import *
from .models import *
import pandas as pd
from django.db.models import Q
from django.views.decorators.http import require_POST
import traceback
from collections import defaultdict
import traceback
import re
from .models import ModuleSettings, School
from .forms import ModuleSettingsForm

def super_home(request):

   return render(request, 'dashboard/dashboard_home.html', )
def dashboard_home(request):
   
    
    return render(request, 'dashboard/dashboard_home.html', )

def academic_module(request, module_code):
    # Get existing module with status 1 (if any)
    existing_module = ModuleSettings.objects.filter(module=module_code, status=1).first()
    print("existing module:",existing_module)
    # If it exists, prefill form with that record
    if existing_module:
        form = ModuleSettingsForm(
            request.POST or None,
            request.FILES or None,
            instance=existing_module
        )
    else:
        # No active record found → create new instance with module_code
        initial_data = {'module': module_code}
        form = ModuleSettingsForm(request.POST or None, request.FILES or None, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            school_selected = form.cleaned_data.get('school')
            module_selected = form.cleaned_data.get('module')
            status_value = form.cleaned_data.get('status')

            existing_record = ModuleSettings.objects.filter(school=school_selected, module=module_selected).first()

            if existing_record:
                # Update status only
                existing_record.status = status_value
                existing_record.save()

                if status_value == 1:
                    messages.success(request, f"✅ '{module_selected}' activated for {school_selected}.")
                else:
                    messages.warning(request, f"⚠️ '{module_selected}' deactivated for {school_selected}.")
            else:
                # If no record exists, create new
                form.save()
                messages.success(request, f"✅ Module '{module_selected}' added successfully for {school_selected}.")

            return redirect('academic_module', module_code=module_code)

    # Fetch all schools for display if needed
    schools = School.objects.all()
    context = {
        'page_title': "Module Settings",
        'form': form,
        'school': schools,
        'module_code': module_code,
        'existing_module': existing_module,
    }
    return render(request, 'dashboard/module_settings.html', context)

 
