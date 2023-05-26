import os
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from datetime import date, timedelta
from multiselectfield import MultiSelectField


################## USER ACCOUNT #####################################################

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mail wymagany.')

        email = self.normalize_email(email) if email else None

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(username, email, password, **extra_fields)
        UserProfile.objects.create(user=user)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    CHOICES = [
        ('W', 'Kobieta'),
        ('M', 'Mężczyzna'),
        ('O', 'Inne')]

    username = models.CharField(unique=True, max_length=150, blank=True)
    email = models.EmailField(unique=True, max_length=255, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    sex = models.CharField(max_length=1, choices=CHOICES, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                        (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            profile, created = UserProfile.objects.get_or_create(user=self)
            profile.age = age
            profile.save()


################## USER PROFILE #####################################################


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


def user_directory_path(instance, filename):
    user_folder = str(instance.user.username)
    return os.path.join('profile_pics', user_folder, filename)


class UserProfile(models.Model):
    SEX_CHOICES = [
        ('W', 'Kobiety'),
        ('M', 'Mężczyzni'),
        ('O', 'Inni'),
        ('A', 'Wszyscy')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField()
    education = models.CharField(max_length=200, blank=True)
    job = models.CharField(max_length=200, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to=user_directory_path)
    languages = models.CharField(max_length=200, blank=True)
    interests = models.CharField(max_length=500, blank=True)
    min_age_preference = models.PositiveIntegerField(blank=True, null=True)
    max_age_preference = models.PositiveIntegerField(blank=True, null=True)
    sex_preference = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)


    def save(self, *args, **kwargs):
        try:
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.profile_pic != self.profile_pic:
                old_profile.profile_pic.delete(save=False)  # Delete the old profile picture from the database
        except UserProfile.DoesNotExist:
            pass
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username



################## WIADOMOŚCI #####################################################

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=80)
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return self.subject

