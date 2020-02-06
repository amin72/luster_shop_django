from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import re


def phone_number_validator(value):
    """
    A phone validator
    """
    if value:
        regex= re.compile('09(0[1-5]|1[0-9]|3[0-9]|2[0-2])-?[0-9]{3}-?[0-9]{4}')
        result = regex.search(value)
        if result is None:
            raise ValidationError(_('Enter a valid phone number'))



class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password, is_superuser=False,
        is_staff=False, is_active=False):

        if not phone_number:
            raise ValueError("I KNOW YOU HAVE A NAME")
        if not password:
            raise ValueError("PASSWORD?!?!?!? HELLO??")

        user = self.model(email=self.normalize_email(email))
        user.phone_number = phone_number
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.save()
        return user

    def create_superuser(self, phone_number, email, password):
        user = self.create_user(phone_number, email, password,
            is_superuser=True, is_staff=True, is_active=True)
        return user



class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11,
        unique=True, verbose_name=_('Phone Number'),
        validators=[phone_number_validator],
        help_text=_('User Phone Number, example: 09123456790'))

    username = models.CharField(_('Username'),
        max_length=40,
        blank=True,
        null=True)


    USERNAME_FIELD = 'phone_number'
    objects = UserManager()


    class Meta:
        unique_together = ('phone_number', 'username', 'email')
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.phone_number}"
