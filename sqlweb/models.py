from django.db import models
from django.contrib.auth.models import User

# 员工基本信息表


class StaffBasicInfo(models.Model):

    staffname = models.CharField(max_length=20,primary_key=True)
    staffstate = models.BooleanField(default=True)
    staffphonenumber = models.IntegerField()
    staffidnumber = models.CharField(max_length=15)
    note = models.TextField(max_length=200)

    class Meta:
        db_table='StaffBasicInfo'

#日考勤表


class Daycheckon(models.Model):

    staffname = models.CharField(max_length=10)                         #姓名
    subject = models.CharField(max_length=10)                        #工地
    Dc_date = models.DateField()                                        #年
    Dc_morning = models.BooleanField()                                  #早上
    Dc_afternoon = models.BooleanField()                                #下午
    Dc_overtime = models.DecimalField(decimal_places=3,max_digits=10)  #加班

    class Meta:
        db_table='Daycheckon'
        unique_together=("staffname","Dc_date")


#员工薪金表


class Salaryset(models.Model):
    S_year = models.IntegerField()
    S_month = models.IntegerField()
    staffname = models.CharField(max_length=10)
    daypay = models.DecimalField(decimal_places=3,max_digits=10)
    OT_pay = models.DecimalField(decimal_places=3,max_digits=10)
    insurance = models.DecimalField(decimal_places=3,max_digits=10)
    subsidy = models.DecimalField(decimal_places=3,max_digits=10)
    other = models.DecimalField(decimal_places=3,max_digits=10)
    note = models.TextField(max_length=1000)

    class Meta:
        db_table = 'Salaryset'
        unique_together=("S_year","S_month","staffname")


#月考勤表
'''
class Monthcheckon(models.Model):
    M_year = models.IntegerField()
    M_month = models.IntegerField()
    subject = models.CharField(max_length=20)
    staffname = models.CharField(max_length=10)
    M_checkonday = models.DecimalField(max_digits=4,decimal_places=2)
    M_overtime = models.DecimalField(max_digits=4,decimal_places=2)

    class Meta:
        db_table='Monthcheckon'
'''

#工地信息表
class subjecttable(models.Model):
    subjectID=models.AutoField(primary_key=True)
    subjectname = models.CharField(max_length=100,unique=True)
    subjectshortname = models.CharField(max_length=15,null=True,unique=True)
    contractnunber= models.CharField(max_length=80,null=True,unique=True)
    subjectsum = models.DecimalField(decimal_places=3,max_digits=15,default=0)
    jia = models.CharField(max_length=15,null=True)
    yi = models.CharField(max_length=15,null=True)
    subjectmanager = models.CharField(max_length=5)
    lvhua = models.BooleanField(default=0)
    yuanjian = models.BooleanField(default=0)
    light = models.BooleanField(default=0)
    shuidian =models.BooleanField(default=0)
    begintime = models.DateField(blank=True,null=True)
    endtime = models.DateField(blank=True,null=True)
    statment = models.CharField(max_length=10,null=True)
    subjectnote = models.TextField(max_length=1000)
    percentage = models.IntegerField(default=0)
    class Meta:
        db_table = 'subjecttable'

#


#以下是物料模板

#物料表

class itemtable(models.Model):
    itemID = models.CharField(max_length=15,primary_key=True)#物料ID
    proposer = models.CharField(max_length=10)#申请人
    subject = models.ForeignKey(subjecttable,on_delete=models.CASCADE)#项目名
    sort = models.CharField(max_length=10)#分类
    beneficiary_name = models.CharField(max_length=30)#收款方
    beneficiary_acc = models.CharField(max_length=25,null=False,default="0000")
    bank = models.CharField(max_length=30,null=True)
    beneficiary_acc_t = models.CharField(max_length=4)#收款方账户类型
    sum_m = models.DecimalField(decimal_places=3,max_digits=15)#金额
    haverbill = models.BooleanField(default=0)#是否提供发票
    detail = models.TextField(max_length=4000)#详细说明
    photo = models.ImageField(upload_to="itemphoto")#图片
    statment = models.CharField(max_length=10)#状态
    class Meta:
        db_table='itemtable'



#申请表

class application(models.Model):
    applicationID = models.CharField(max_length=15,primary_key=True)#申请iD
    itemID = models.ForeignKey(itemtable,on_delete=models.CASCADE)#物料id
    S_pay_name = models.CharField(max_length=30)#转出账户
    S_pay_accounnt_type = models.CharField(max_length=4)#转出账户类型
    account_suggest = models.CharField(max_length=100)#会计部意见
    multiple_suggest = models.CharField(max_length=100)#综合部意见
    audit_suggest = models.CharField(max_length=100)#审计部意见
    final_sum = models.DecimalField(decimal_places=3,max_digits=15)#批准金额
    ceo_suggest = models.CharField(max_length=100)#总经理意见
    statment = models.CharField(max_length=5)#申请状态

#收款方信息表

class Bankaccount(models.Model):
    accountname = models.CharField(max_length=20)#账户名
    bankname = models.CharField(max_length=25)#所属银行
    subbankname = models.CharField(max_length=30)#所属支行
    accountnumber = models.CharField(max_length=20,primary_key=True)#银行账号
    company = models.CharField(max_length=30)#所属公司
    accountstyle = models.CharField(max_length=10)#账户类型
    detail = models.TextField(max_length=100)#备注


    
class paybill(models.Model):
    paybillID = models.CharField(max_length=15,primary_key=True)#转账ID
    paytime = models.DateField()#转账时间
    applicationID = models.ForeignKey(application,on_delete=models.CASCADE)#申请ID
    pay_name = models.CharField(max_length=30)#转出账户
    pay_accounnt_type = models.CharField(max_length=4)#转出账户类型
    accountnunber = models.ForeignKey(Bankaccount,on_delete=models.CASCADE)#收款方账户
    sum_m = models.DecimalField(decimal_places=3,max_digits=15)#转账金额



class useradd(models.Model):
     username = models.OneToOneField(User,on_delete=models.CASCADE)
     name_zh = models.CharField(max_length=10)
     job = models.CharField(max_length=10)
     class Meta:
         verbose_name_plural = "useradd"
         db_table = 'useradd'


class itemimage(models.Model):
    imageid = models.AutoField(primary_key=True)
    item = models.ForeignKey(itemtable,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='itemimage/%Y/%m/%d')