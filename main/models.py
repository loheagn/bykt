from django.db import models

# Create your models here.


class Student(models.Model):
    studentID = models.IntegerField(unique=False)
    name = models.CharField(max_length=128, unique=False)
    password = models.CharField(max_length=256)
    face_array = models.TextField(unique=True, null=False)
    visit = models.IntegerField(unique=False, null=False, default=0)
    volunteer = models.IntegerField(unique=False, null=False, default=0)
    old_volunteer = models.IntegerField(unique=False, null=False, default=0)
    sport = models.FloatField(unique=False, null=False, default=0.0)
    my_article = models.BooleanField(unique=False, null=False, default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.studentID)

    class Meta:
        ordering = ["studentID"]
        verbose_name = "Student"
        verbose_name_plural = "Student"


class ProfileImage(models.Model):
    image = models.ImageField(null=False, upload_to="images/profile")


class TmpImage(models.Model):
    image = models.ImageField(null=False, upload_to="images/tmp", unique=False)


class Article(models.Model):
    articleID = models.AutoField(primary_key=True)
    authorName = models.CharField(max_length=128)
    articleTitle = models.CharField(max_length=128, unique=False)
    articleContent = models.TextField()
    articlecopyContent = models.TextField()
    article_copy_rate = models.FloatField()
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True)


class VisitImage(models.Model):
    image = models.ImageField(null=False, unique=True, upload_to="images/visit")
    is_ok = models.BooleanField(null=False, unique=False)
    similar = models.FloatField(null=False, unique=False)
    v_time = models.DateField(null=False)
    location = models.CharField(max_length=256, null=False)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=False)
    string_array = models.TextField(null=False, default="", unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.studentID


class SportImage(models.Model):
    image = models.ImageField(null=False, unique=True, upload_to="images/sport")
    s_time = models.DateTimeField(null=False, unique=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=False)
    number = models.FloatField(unique=False, null=False)
    content = models.TextField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

