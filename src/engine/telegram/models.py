from django.db import models
from core.models import Language, CartBase, Settings, OrderBase, BranchBase
from django.utils import timezone
import hashlib

# Create your models here.


class PaySystem(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    token = models.CharField(
        'Token',
        max_length=1024,
        null=False,
        blank=False
        )

    currency = models.CharField(
        'Currency',
        max_length=10,
        default="",
        null=False,
        blank=False
        )

    eq = models.IntegerField(
        'PaySystem Equalizer',
        default=100,
        blank=False,
        null=False
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

    chat_id = models.BigIntegerField(
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

    real_name = models.CharField(
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

    phone = models.BigIntegerField(
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

    def full_name(self):
        return f'{self.first_name} {self.last_name}' \
            if self.last_name is not None \
            else self.first_name

    def __str__(self):
        return self.full_name()


class Cart(CartBase):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selected_user'
        )


class Settings(Settings):

    def __str__(self):
        return self.title


class Order(OrderBase):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )

    latitude = models.FloatField(
        'Latitude',
        default=0.0,
        null=False,
        blank=False
    )

    longitude = models.FloatField(
        'Longitude',
        default=0.0,
        null=False,
        blank=False
    )

    paysystem = models.ForeignKey(
        PaySystem,
        default=None,
        on_delete=models.CASCADE,
        related_name='paysystem_telegram_order',
        null=True,
        blank=True
        )

    selected_branch = models.ForeignKey(
        'Branch',
        default=None,
        on_delete=models.CASCADE,
        related_name='selected_branch_telegram_order',
        null=True,
        blank=True
        )

    manager = models.ForeignKey(
        User,
        default=None,
        on_delete=models.CASCADE,
        related_name='manager_telegram_order',
        null=True,
        blank=True
        )

    address = models.TextField(
        'Posible Address',
        default="",
        blank=False,
        null=False
        )

    paid_at = models.DateTimeField(
        'Created at',
        # auto_now_add=True,
        null=True,
        blank=True
        )
    
    paid = models.BooleanField(
        default=False
    )

    def get_price(self):

        total = 0

        for position in self.cart.positions.all():
            total += position.get_price()
        return total

    def get_count(self):

        count = 0

        for position in self.cart.positions.all():
            count += position.count
        return count


class Branch(BranchBase):

    latitude = models.FloatField(
        'Latitude',
        default=0.0,
        null=False,
        blank=False
    )

    default = models.BooleanField(
        default=False
    )

    external_id = models.IntegerField(
        'External ID',
        default=0,
        blank=True,
        null=True
        )

    longitude = models.FloatField(
        'Longitude',
        default=0.0,
        null=False,
        blank=False
    )

    managers = models.ManyToManyField(
        User,
        blank=True
        )

    channel = models.BigIntegerField(
        'Channel Id',
        default=0,
        blank=False,
        null=False
        )


    # def __str__(self):
    #     return self.title
