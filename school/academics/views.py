from django.urls import reverse_lazy
from core.views import SmartCreateView, SmartListView
from .models import Student

class StudentCreateView(SmartCreateView):
    model = Student
    # These names must match models.py exactly
    fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade_level']
    success_url = reverse_lazy('academics:student-list')
    extra_context = {'page_title': 'Enroll New Student'}

class StudentListView(SmartListView):
    model = Student