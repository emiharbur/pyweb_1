from django.db import models

class StaffBaseInfo(models.Model):
    stuffname = models.CharField(max_length=20,primary_key=True)
    stuffstate = models.BooleanField(default=True)
    stuffaccount = models.CharField(max_length=20)
    stuffphonenumber = models.IntegerField(max_length=20)
    stuffremark = models.TextField()

class DateWorkrec(models.Model):
    stuffname = models.CharField(max_length=10)
    wtdate = models.DateField()
    worksite = models.CharField(max_length=10)
    workstate = models.BooleanField()
    overtime = models.DecimalField()

class Salary(models.Model):
    SaDate = models.DateField()
    SaName = models.CharField()
    msalay = models.IntegerField()
    overtimepay = models.DecimalField()
    insurance = models.DecimalField()
    subsidy = models.DecimalField()
    other = models.DecimalField()

class Bankaccount(models.Model):
    accountname = models.CharField()
    bankname = models.CharField()
    accountnumber = models.CharField()
    accountgroup = models.CharField()
    detail = models.TextField()
    





# Create your models here.
