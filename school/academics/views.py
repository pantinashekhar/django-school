from django.urls import reverse_lazy
from core.views import SmartCreateView, SmartListView
from .models import Student

class StudentCreateView(SmartCreateView):
    model = Student
    # These fields must match your models.py
    fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date', 'grade_level']
    
    # Redirect to the list after adding
    success_url = reverse_lazy('academics:student-list')
    
    extra_context = {
        'page_title': 'Enroll New Student',
        'btn_text': 'Confirm Enrollment'
    }

class StudentListView(SmartListView):
    model = Student