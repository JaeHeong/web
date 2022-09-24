from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField('date published', default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField('date published', auto_now = True)

class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField('date published', default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField('date published', auto_now = True)

    def __str__(self):
        return self.title