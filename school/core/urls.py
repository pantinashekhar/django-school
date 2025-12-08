from django.urls import path
from .views import StudentCreateView,CourseCreateView,EnrollmentStudentView,StudentDetailView,CourseDetailView



urlpatterns = [path("students/add",StudentCreateView.as_view()),
               path("courses/add",CourseCreateView.as_view()),
               path("enroll/",EnrollmentStudentView.as_view()),
               path("students/<int:pk>",StudentDetailView.as_view()),
               path("courses/<int:pk>",CourseDetailView.as_view())]