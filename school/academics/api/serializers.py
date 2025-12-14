from rest_framework import serializers
from academics.models import Student, Grade


class AcademicStudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "date_of_birth",
            "enrollment_date",
            "grade_level",
        ]
        read_only_fields = ["enrollment_date"]

    def get_full_name(self, obj:Student) -> str:
        return f"{obj.first_name} {obj.last_name}"


class GradeSerializer(serializers.ModelSerializer):
    student = AcademicStudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True,
    )

    class Meta:
        model = Grade
        fields = [
            "id",
            "student",
            "student_id",
            "subject",
            "score",
            "date_recorded",
        ]
        read_only_fields = ["date_recorded"]
