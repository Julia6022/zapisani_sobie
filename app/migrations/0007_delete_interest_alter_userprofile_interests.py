# Generated by Django 4.2 on 2023-05-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_userprofile_interests_userprofile_interests'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Interest',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
