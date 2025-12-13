from django.urls import path,include
from . import views

app_name = 'academics'

urlpatterns = [
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-create'),
]