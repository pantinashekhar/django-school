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
from .models import Student,Enrollment
from rest_framework import generics
from .serializers import EnrollmentSerializer

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

# src/core/views.py

class SmartCreateView(AdaptableCRUDBase, LoginRequiredMixin, CreateView):
    template_name = "core/generic_form.html" # (or generic_form_modal.html)

    def get_success_url(self):
        # 1. If the developer explicitly set success_url in the subclass, use it.
        if self.success_url:
            return self.success_url

        # 2. Otherwise, generate it intelligently using the App Namespace
        app_label = self.model._meta.app_label 
        model_name = self.model._meta.model_name
        
        # This generates 'academics:student-list' instead of just 'student-list'
        return reverse_lazy(f"{app_label}:{model_name}-list")

class IndexView(TemplateView):
    template_name = "core/index.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. REAL: Count total students in database
        total_students = Student.objects.count()
        context['total_students'] = total_students
        
        # 2. REAL: Calculate stats for the widgets
        # Example: Count new students joined this month?
        # For now, let's keep revenue simulated based on student count (e.g. $100 per student)
        estimated_revenue = total_students * 100 
        context['revenue'] = estimated_revenue
        
        # 3. REAL: Recent enrollments (Last 5 students)
        context['recent_students'] = Student.objects.order_by('-enrollment_date')[:5]
        
        return context

class UniversalDeleteView(LoginRequiredMixin, View):
    def delete(self, request, app_label, model_name, pk):
        """
        Deletes any object dynamically based on URL parameters.
        HTMX sends a DELETE request here.
        """
        try:
            # 1. Find the Model (e.g., look for 'Student' inside 'academics')
            ModelClass = apps.get_model(app_label, model_name)
            
            # 2. Find the specific record (ID)
            obj = get_object_or_404(ModelClass, pk=pk)
            
            # 3. Delete it
            obj.delete()
            
            # 4. Return 200 OK. 
            # HTMX will see this and execute the swap (removing the row).
            return HttpResponse(status=200)
            
        except LookupError:
            return HttpResponse(status=404)
        


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "core/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get count of students per grade level
        # Output example: <QuerySet [{'grade_level': 1, 'total': 5}, {'grade_level': 2, 'total': 3}]>
        stats = Student.objects.values('grade_level').annotate(total=Count('id')).order_by('grade_level')
        
        # Pass separate lists to Chart.js
        # We add "Grade " prefix so the chart looks nice (e.g. "Grade 1")
        context['labels'] = [f"Grade {item['grade_level']}" for item in stats]
        context['data'] = [item['total'] for item in stats]
        
        return context
    
class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = Enrollment.objects.all()
        student_id = self.request.query_params.get('student_id')
        course_id = self.request.query_params.get('course_id')
        
        if student_id:
            queryset = queryset.filter(student__id=student_id)
        if course_id:
            queryset = queryset.filter(course__id=course_id)
        return queryset