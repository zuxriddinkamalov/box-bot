from django.db import models
from django.utils import timezone

# Create your models here.


class Language(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    def __str__(self):
        return self.title


class Settings(models.Model):

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

    token = models.CharField(
        'Token',
        max_length=1024,
        null=False,
        blank=False
        )

    chatbase_token = models.CharField(
        'Chatbase Token',
        max_length=1024,
        null=True,
        blank=True
        )

    def __str__(self):
        return self.title


class Message(models.Model):

    number = models.IntegerField(
        'Message Number',
        default=0,
        blank=False,
        null=False
        )

    title = models.CharField(
        'Title',
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='message_language'
        )

    text = models.TextField(
        'Text',
        default=None,
        blank=False,
        null=False
        )

    def __str__(self):
        return f'{self.language.title} {self.title}'


class Button(models.Model):

    order = models.IntegerField(
        'Button Number',
        default=0,
        blank=False,
        null=False
        )

    button_code = models.CharField(
        'Button unique code',
        max_length=512,
        default=None,
        blank=False,
        null=False
        )

    title = models.CharField(
        'Title',
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    checkpoint = models.IntegerField(
        'Button checkpoint group',
        default=1,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        related_name='button_language'
        )

    def __str__(self):
        return f'{self.language.title} {self.title}'


class Photo(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    file_id = models.CharField(
        'Telegram File ID',
        max_length=1024,
        default=None,
        blank=True,
        null=True
        )

    photo = models.ImageField(
        'Photo',
        upload_to='media/property'
        )

    def __str__(self):
        return f'{self.id} - {self.file_id}'


class Announcement(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="news_language"
        )

    text = models.TextField(
        'Announcement text',
        null=True,
        blank=True
        )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
        )

    views = models.PositiveIntegerField(
        'Views',
        default=0,
        blank=True,
        null=True
        )

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        null=False,
        blank=False
        )

    updated_at = models.DateTimeField(
        'Last view',
        auto_now=True,
        null=False,
        blank=False)

    active = models.BooleanField(
        "Active",
        default=False,
        blank=False,
        null=False
        )

    visible = models.BooleanField(
        "Visible",
        default=False,
        blank=False,
        null=False
        )

    def __str__(self):
        return f'{self.language.title} - {self.title}'

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(Announcement, self).save(*args, **kwargs)


class Event(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="event_language"
        )

    text = models.TextField(
        'Event text',
        blank=True,
        null=True
        )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
        )

    views = models.PositiveIntegerField(
        'Views',
        default=0,
        blank=True,
        null=True
        )

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        null=False,
        blank=False
        )

    updated_at = models.DateTimeField(
        'Last view',
        auto_now=True,
        null=False,
        blank=False)

    active = models.BooleanField(
        "Active",
        default=False,
        blank=False,
        null=False
        )

    visible = models.BooleanField(
        "Visible",
        default=False,
        blank=False,
        null=False
        )

    def __str__(self):
        return f'{self.language.title} - {self.title}'

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(Event, self).save(*args, **kwargs)


class Category(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="category_language"
        )

    description = models.TextField(
        'Description',
        default=None,
        blank=False,
        null=False
        )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
        )

    active = models.BooleanField(
        "Active",
        default=False,
        blank=False,
        null=False
        )

    order = models.IntegerField(
        'Category Number',
        default=0,
        blank=False,
        null=False
        )


class Product(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="product_language"
        )

    description = models.TextField(
        'Description',
        default=None,
        blank=False,
        null=False
        )

    price = models.IntegerField(
        'Price',
        default=0,
        blank=False,
        null=False
        )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
        )

    active = models.BooleanField(
        "Active",
        default=False,
        blank=False,
        null=False
        )

    order = models.IntegerField(
        'Product Number',
        default=0,
        blank=False,
        null=False
        )


class Position(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
        )

    count = models.IntegerField(
        "Product count",
        default=1,
        blank=False,
        null=False
        )

    @classmethod
    def get_price(self):

        price_per_one = self.product.price
        price = price_per_one * self.count

        return price
