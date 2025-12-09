from django.urls import path
from .views import add_student_form,add_course_form,enroll_student_form,list_courses,list_students,enrollment_student
#StudentCreateView,CourseCreateView,EnrollmentStudentView,StudentDetailView,CourseDetailView



urlpatterns = [path("student/add-form",add_student_form,name="add_student_form"),
               path("students/",list_students,name="list_students"),
               path("courses/add-form",add_course_form,name="add_course_form"),
               path("courses/",list_courses,name="list_courses"),
               path("enroll/",enroll_student_form,name="enroll_student_form"),
               path("enrollment_success/",enrollment_student,name="enrollment_success"),
               ]