from django.db import models

# Create your models here.


class Student(models.Model):
    studentID = models.IntegerField(unique=False)
    name = models.CharField(max_length=128, unique=False)
    password = models.CharField(max_length=256)
    face_array = models.TextField(unique=True, null=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.studentID)

    class Meta:
        ordering = ["studentID"]
        verbose_name = "Student"
        verbose_name_plural = "Student"


class ProfileImage(models.Model):
    image = models.ImageField(null=True, upload_to="images/profile")
