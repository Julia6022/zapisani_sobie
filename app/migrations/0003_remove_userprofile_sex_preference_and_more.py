# Generated by Django 4.2 on 2023-05-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='sex_preference',
        ),
        migrations.DeleteModel(
            name='SexPreference',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sex_preference',
            field=models.CharField(blank=True, choices=[('W', 'Kobiety'), ('M', 'Mężczyzni'), ('O', 'Inni'), ('A', 'Wszyscy')], max_length=1),
        ),
    ]