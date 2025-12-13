from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.apps import apps
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from users.permissions import RoleRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Import your models dynamically to avoid circular imports if possible, 
# or import them directly if structure allows.
from academics.models import Student

class AdaptableCRUDBase:
    """
    Base Mixin that automatically gathers model fields and configures
    templates to work with HTMX.
    """
    template_name = "core/generic_list.html"  # Single template for ALL lists
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.model
        
        # 1. Setup Columns (Existing logic)
        context['columns'] = [f.name for f in model._meta.fields if f.name != 'id']
        context['verbose_names'] = [f.verbose_name.title() for f in model._meta.fields if f.name != 'id']
        context['model_name'] = model._meta.verbose_name
        context['model_name_plural'] = model._meta.verbose_name_plural
        
        # 2. SMART URL GENERATION (The Fix)
        # Automatically detects 'academics' from the model
        app_label = model._meta.app_label 
        model_name = model._meta.model_name
        
        # Generates 'academics:student-create' automatically
        context['create_url'] = reverse_lazy(f"{app_label}:{model_name}-create")
        
        return context

class SmartListView(AdaptableCRUDBase, LoginRequiredMixin, ListView):
    paginate_by = 10

class SmartCreateView(AdaptableCRUDBase, LoginRequiredMixin, CreateView):
    template_name = "core/generic_list.html" # HTMX Modal form

    def get_success_url(self):
        return reverse_lazy(f"{self.model._meta.model_name}-list")

class IndexView(TemplateView):
    template_name = "core/index.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add high-level stats here for the dashboard widgets
        # context['total_students'] = ... 
        return context

class UniversalDeleteView(RoleRequiredMixin, View):
    """
    Advanced Generic View: Deletes any object based on URL parameters.
    Greatly reduces boilerplate code.
    """
    # Only Admins/Principals should be able to use the raw generic delete
    # Or you can add logic to check per-model permissions.
    required_roles = ['Admin', 'Principal'] 
    
    def delete(self, request, app_label, model_name, pk):
        try:
            # Dynamically get the model class (e.g., Student, Grade)
            ModelClass = apps.get_model(app_label, model_name)
            obj = get_object_or_404(ModelClass, pk=pk)
            
            # Security Check: Ensure the user actually has permission to delete THIS specific object
            # (Optional: integrate logic from users/permissions.py here)
            
            obj.delete()
            
            # Return empty response (200 OK). 
            # HTMX will see this and remove the row from the HTML table automatically.
            return HttpResponse("") 
            
        except LookupError:
            return HttpResponseForbidden("Invalid Model")
        


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "core/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Example Report: Count students by Grade Level (assuming you have a 'grade' field)
        # Adjust 'grade' to whatever field name you actually use in your Student model
        enrollment_stats = Student.objects.values('grade_level').annotate(total=Count('id')).order_by('grade_level')
    
        # Update the list comprehension to match the new field name
        context['labels'] = [item['grade_level'] for item in enrollment_stats]
        context['data'] = [item['total'] for item in enrollment_stats]
    
        
        return context