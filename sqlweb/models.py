from django.db import models

class StaffBaseInfo(models.Model):
    stuffname = models.CharField(max_length=20,primary_key=True)
    stuffstate = models.BooleanField(default=True)
    stuffaccount = models.CharField(max_length=20)
    stuffphonenumber = models.IntegerField(max_length=20)
    stuffremark = models.TextField()

# Create your models here.
