from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .manager import CustomUserManager
from datetime import datetime, timedelta
USERNAME_REGEX = r'^[\w.@+\- ]+$'

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, validators=[RegexValidator(
        regex=USERNAME_REGEX, message='الاسم يجب ان يتكون من احرف و ارقام', code='invalid_username')])
    birthdate=models.DateField(null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$', message="الرقم غير صحيح برجاء ادخال رقم صحيح")

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True




class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="period_user")
    start_date = models.DateTimeField()
    days = models.JSONField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        day ={}
        for i in range(10):
            a_date = (self.start_date + timedelta(days = i))
            day.update({i: a_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")})
        self.days = day
        super(Period, self).save(*args, **kwargs)