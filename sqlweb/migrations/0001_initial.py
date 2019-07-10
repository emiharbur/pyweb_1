# Generated by Django 2.1 on 2019-07-04 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='application',
            fields=[
                ('applicationID', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('S_pay_name', models.CharField(max_length=30)),
                ('S_pay_accounnt_type', models.CharField(max_length=4)),
                ('account_suggest', models.CharField(max_length=100)),
                ('multiple_suggest', models.CharField(max_length=100)),
                ('audit_suggest', models.CharField(max_length=100)),
                ('final_sum', models.DecimalField(decimal_places=3, max_digits=15)),
                ('ceo_suggest', models.CharField(max_length=100)),
                ('statment', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Bankaccount',
            fields=[
                ('accountname', models.CharField(max_length=20)),
                ('bankname', models.CharField(max_length=20)),
                ('subbankname', models.CharField(max_length=30)),
                ('accountnumber', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=30)),
                ('accountstyle', models.SmallIntegerField()),
                ('detail', models.TextField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Daycheckon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staffname', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=10)),
                ('Dc_date', models.DateField()),
                ('Dc_morning', models.BooleanField()),
                ('Dc_afternoon', models.BooleanField()),
                ('Dc_overtime', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
            options={
                'db_table': 'Daycheckon',
            },
        ),
        migrations.CreateModel(
            name='itemtable',
            fields=[
                ('itemID', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('proposer', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=20)),
                ('sort', models.CharField(max_length=10)),
                ('beneficiary_name', models.CharField(max_length=30)),
                ('beneficiary_acc_t', models.CharField(max_length=4)),
                ('sum_m', models.DecimalField(decimal_places=3, max_digits=15)),
                ('haverbill', models.BooleanField(default=0)),
                ('detail', models.TextField(max_length=4000)),
                ('photo', models.ImageField(upload_to='itemphoto')),
                ('statment', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'itemtable',
            },
        ),
        migrations.CreateModel(
            name='paybill',
            fields=[
                ('paybillID', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('paytime', models.DateField()),
                ('pay_name', models.CharField(max_length=30)),
                ('pay_accounnt_type', models.CharField(max_length=4)),
                ('sum_m', models.DecimalField(decimal_places=3, max_digits=15)),
                ('accountnunber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqlweb.Bankaccount')),
                ('applicationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqlweb.application')),
            ],
        ),
        migrations.CreateModel(
            name='Salaryset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('S_year', models.IntegerField()),
                ('S_month', models.IntegerField()),
                ('staffname', models.CharField(max_length=10)),
                ('daypay', models.DecimalField(decimal_places=3, max_digits=10)),
                ('OT_pay', models.DecimalField(decimal_places=3, max_digits=10)),
                ('insurance', models.DecimalField(decimal_places=3, max_digits=10)),
                ('subsidy', models.DecimalField(decimal_places=3, max_digits=10)),
                ('other', models.DecimalField(decimal_places=3, max_digits=10)),
                ('note', models.TextField(max_length=1000)),
            ],
            options={
                'db_table': 'Salaryset',
            },
        ),
        migrations.CreateModel(
            name='StaffBasicInfo',
            fields=[
                ('staffname', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('staffstate', models.BooleanField(default=True)),
                ('staffphonenumber', models.IntegerField()),
                ('staffidnumber', models.CharField(max_length=15)),
                ('note', models.TextField(max_length=200)),
            ],
            options={
                'db_table': 'StaffBasicInfo',
            },
        ),
        migrations.CreateModel(
            name='subjecttable',
            fields=[
                ('subjectID', models.AutoField(primary_key=True, serialize=False)),
                ('subjectname', models.CharField(max_length=20)),
                ('subjectshortname', models.CharField(max_length=15, null=True)),
                ('contractnunber', models.CharField(max_length=40, null=True)),
                ('subjectsum', models.IntegerField()),
                ('jia', models.CharField(max_length=15, null=True)),
                ('yi', models.CharField(max_length=15, null=True)),
                ('subjectmanager', models.CharField(max_length=5)),
                ('lvhua', models.BooleanField(default=0)),
                ('yuanjian', models.BooleanField(default=0)),
                ('light', models.BooleanField(default=0)),
                ('shuidian', models.BooleanField(default=0)),
                ('begintime', models.DateField(blank=True, null=True)),
                ('endtime', models.DateField(blank=True, null=True)),
                ('statment', models.CharField(max_length=10, null=True)),
                ('subjectnote', models.TextField(max_length=1000)),
                ('percentage', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'subjecttable',
            },
        ),
        migrations.CreateModel(
            name='useradd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_zh', models.CharField(max_length=10)),
                ('job', models.CharField(max_length=10)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'useradd',
                'db_table': 'useradd',
            },
        ),
        migrations.AlterUniqueTogether(
            name='salaryset',
            unique_together={('S_year', 'S_month', 'staffname')},
        ),
        migrations.AlterUniqueTogether(
            name='daycheckon',
            unique_together={('staffname', 'Dc_date')},
        ),
        migrations.AddField(
            model_name='application',
            name='itemID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqlweb.itemtable'),
        ),
    ]