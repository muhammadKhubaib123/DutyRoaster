from django.db import models

# Create your models here.
class FilesUpload(models.Model):
    file=models.FileField()

class RoasterTables(models.Model):

    table_name = models.CharField(max_length = 120)
    shift = models.IntegerField()