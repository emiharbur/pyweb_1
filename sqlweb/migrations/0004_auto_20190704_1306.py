# Generated by Django 2.1 on 2019-07-04 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlweb', '0003_auto_20190704_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjecttable',
            name='contractnunber',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='subjecttable',
            name='subjectname',
            field=models.CharField(max_length=100),
        ),
    ]
