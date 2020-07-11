from django.db import models
from core.models import Language, CartBase
from django.utils import timezone


# Create your models here.


class PaySystem(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    active = models.BooleanField(
        'Active',
        default=True,
        null=False,
        blank=False
        )

    order = models.IntegerField(
        'PaySystem Number',
        default=0,
        blank=False,
        null=False
        )

    def __str__(self):
        return self.title


class User(models.Model):

    chat_id = models.IntegerField(
        'Chat id',
        default=0,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='user_language'
        )

    first_name = models.CharField(
        'First Name',
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    last_name = models.CharField(
        'Last Name',
        default=None,
        max_length=255,
        blank=True,
        null=True
        )

    username = models.CharField(
        'Username',
        default=None,
        max_length=255,
        blank=True,
        null=True
        )

    phone = models.PositiveIntegerField(
        'Phone',
        default=None,
        blank=True,
        null=True
        )

    language_set = models.BooleanField(
        'Language set',
        default=False,
        blank=True,
        null=True
        )

    createdAt = models.DateTimeField(
        'Created at',
        default=timezone.now,
        null=False,
        blank=False
        )

    @classmethod
    def full_name(self):
        return f'{self.first_name} {self.last_name}' \
            if self.last_name is not None \
            else self.first_name

    def __str__(self):
        return self.full_name()


class Cart(CartBase):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
