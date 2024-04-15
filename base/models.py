from django.db import models


from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Seperate

import datetime

# Create your models here.

def send_expire_date(increase_day=1, increase_month=1):
    today_date = datetime.date.today()
    final = today_date.replace(month=today_date.month+(increase_month)).replace(day=today_date.day+(increase_day))

    return final


class GuestUser(AbstractUser):


    start_allowed_date =  models.DateField(default=datetime.date.today, null=True, blank=True)
    end_allowed_date =  models.DateField(default=send_expire_date(), null=True, blank=True)

    @property
    def allowed_for_open_gate(self):
        return datetime.date.today() < self.end_allowed_date

    first_name = models.CharField(max_length=300, null=False, blank=False, primary_key=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'first_name'
    REQUIRED_FIELDS = ['last_name']


    def __str__(self):
        return self.email

class Opening(models.Model):
    open_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    opened_by = models.CharField(max_length=300, null=True, blank=True)




    def __str__(self):
        return self.opened_by