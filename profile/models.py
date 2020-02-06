from django.db import models
from django.contrib.auth.models import AbstractUser
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

    class Meta:
        unique_together = ('phone_number', 'username', 'email')
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.phone_number}"
