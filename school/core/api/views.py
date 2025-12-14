from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    EnrollmentSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List students"),
    retrieve=extend_schema(summary="Retrieve a student"),
    create=extend_schema(summary="Create a student"),
    update=extend_schema(summary="Update a student"),
    partial_update=extend_schema(summary="Partially update a student"),
    destroy=extend_schema(summary="Delete a student"),
)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer

    @extend_schema(summary="List courses for a student", responses=CourseSerializer(many=True))
    @action(detail=True, methods=["get"], url_path="courses")
    def courses(self, request, pk=None):
        enrollments = Enrollment.objects.filter(student_id=pk).select_related("course")
        courses = [e.course for e in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="List courses"),
    retrieve=extend_schema(summary="Retrieve a course"),
    create=extend_schema(summary="Create a course"),
    update=extend_schema(summary="Update a course"),
    partial_update=extend_schema(summary="Partially update a course"),
    destroy=extend_schema(summary="Delete a course"),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer

    @extend_schema(summary="List students enrolled in this course", responses=StudentSerializer(many=True))
    @action(detail=True, methods=["get"], url_path="students")
    def students(self, request, pk=None):
        enrollments = Enrollment.objects.filter(course_id=pk).select_related("student")
        students = [e.student for e in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="List enrollments"),
    retrieve=extend_schema(summary="Retrieve an enrollment"),
    create=extend_schema(summary="Create an enrollment"),
    destroy=extend_schema(summary="Delete an enrollment"),
)
class EnrollmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Enrollment.objects.select_related("student", "course").all().order_by("-enrolled_on")
    serializer_class = EnrollmentSerializer
