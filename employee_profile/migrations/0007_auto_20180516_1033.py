# Generated by Django 2.0.3 on 2018-05-16 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0006_auto_20180513_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='employee_profile.Employee'),
        ),
    ]
