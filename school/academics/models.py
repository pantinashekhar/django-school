from django.db import models
from django.utils import timezone

class Student(models.Model):
    # --- THESE LINES MUST BE INDENTED ---
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(default=timezone.now)
    grade_level = models.IntegerField(default=1, help_text="e.g. 1-12")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Grade(models.Model):
    # --- THESE LINES MUST BE INDENTED ---
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"