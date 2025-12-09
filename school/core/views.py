from django.shortcuts import render,redirect
from rest_framework import generics
from .models import Student,Course,Enrollment
# from .serializers import StudentSerializer,CourseSerializer,StudentDetailSerializer,CourseDetailSerializer,EnrollmentSerializer
from .forms import StudentForm,CourseForm,EnrollmentForm


# Create your views here.
# class StudentCreateView(generics.CreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


# class CourseCreateView(generics.CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer


# class EnrollmentStudentView(generics.CreateAPIView):
#     queryset = Enrollment.objects.all()
#     serializer_class = EnrollmentSerializer


# class StudentDetailView(generics.RetrieveAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentDetailSerializer


# class CourseDetailView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseDetailSerializer


def add_student_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_students")
    else:
        form = StudentForm()

    return render(request,"core/add_student.html",{"form":form})          

def list_students(request):
    students = Student.objects.all()
    return render(request,"core/list_students.html",{"students":students})


def add_course_form(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_courses")
    else:
        form = CourseForm()
    return render(request,"core/add_course.html",{"form":form})


def list_courses(request):
    courses = Course.objects.all()
    return render(request,"core/list_courses.html",{"courses":courses})

def enroll_student_form(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enrollment_success")
    else:
        form = EnrollmentForm()
    return render(request,"core/enrollment_student.html",{"form":form})


def enrollment_student(request):
    success = Enrollment.objects.all()
    return render(request,"core/enrollment_success.html",{"success":success})            