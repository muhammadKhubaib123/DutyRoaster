from django.db import models

# Create your models here.
class FilesUpload(models.Model):
    file=models.FileField()

class Table(models.Model):
    table_name = models.CharField(max_length = 120)
class RTable(models.Model):
    table_name = models.CharField(max_length = 130)
class newTable(models.Model):
    table_name = models.CharField(max_length = 130)
class seatingplan(models.Model):
    Room = models.CharField(max_length = 130)
    Total = models.IntegerField()
    Date = models.CharField(max_length = 130)
    Shift = models.CharField(max_length = 130)
class Faculty(models.Model):
    Name = models.CharField(max_length = 130)
    Post = models.CharField(max_length = 130)
