# Generated by Django 2.1 on 2019-07-08 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sqlweb', '0005_auto_20190704_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtable',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqlweb.subjecttable'),
        ),
        migrations.AlterField(
            model_name='subjecttable',
            name='contractnunber',
            field=models.CharField(max_length=80, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='subjecttable',
            name='subjectname',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='subjecttable',
            name='subjectshortname',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
