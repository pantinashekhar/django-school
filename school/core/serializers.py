from rest_framework import serializers
from .models import Student,Course,Enrollment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"



class StudentDetailSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
          model = Student
          fields = ["id","name","email","courses"]

    def get_courses(self,obj):
        enrollments = Enrollment.objects.filter(student=obj)

        return [en.course.title for en in enrollments ]
    

class CourseDetailSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"


    def get_students(self,obj):
        enrollments = Enrollment.objects.filter(course=obj)
        return [ en.student.name for en in enrollments]


