from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    "Many to Many with Extra Fields"
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)


    class Meta:
        unique_together = ('student','course')

    def __str__(self):
        return f"{self.student}->{self.course}"  

    
              