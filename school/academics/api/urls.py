from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcademicStudentViewSet, GradeViewSet

app_name = "academics_api"

router = DefaultRouter()
router.register(r"students", AcademicStudentViewSet, basename="academic-student")
router.register(r"grades", GradeViewSet, basename="grade")

urlpatterns = [
    path("", include(router.urls)),
]
