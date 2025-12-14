from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from academics.models import Student, Grade
from .serializers import AcademicStudentSerializer, GradeSerializer


@extend_schema_view(
    list=extend_schema(summary="List academic students"),
    retrieve=extend_schema(summary="Retrieve an academic student"),
    create=extend_schema(summary="Create an academic student"),
    update=extend_schema(summary="Update an academic student"),
    partial_update=extend_schema(summary="Partially update an academic student"),
    destroy=extend_schema(summary="Delete an academic student"),
)
class AcademicStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("-enrollment_date", "-id")
    serializer_class = AcademicStudentSerializer

    @extend_schema(
        summary="List grades for a student",
        responses=GradeSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="grades")
    def grades(self, request, pk=None):
        grades = Grade.objects.filter(student_id=pk).order_by("-date_recorded")
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="List grades"),
    retrieve=extend_schema(summary="Retrieve a grade"),
    create=extend_schema(summary="Create a grade"),
    update=extend_schema(summary="Update a grade"),
    partial_update=extend_schema(summary="Partially update a grade"),
    destroy=extend_schema(summary="Delete a grade"),
)
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related("student").all().order_by("-date_recorded", "-id")
    serializer_class = GradeSerializer
