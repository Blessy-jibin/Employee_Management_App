# Generated by Django 2.0.3 on 2018-05-16 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0008_auto_20180516_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
