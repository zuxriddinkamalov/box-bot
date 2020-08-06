from django.db import models
from django.utils import timezone
import hashlib

# Create your models here.


class Config(models.Model):

    days_left = models.IntegerField(
        'Days Left',
        default=0,
        blank=False,
        null=False
        )


class Language(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    text = models.CharField(
        'Text',
        max_length=255,
        default=""
        )

    order = models.IntegerField(
        'Language Number',
        default=0,
        blank=False,
        null=False
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

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:

                for language in Language.objects.all():

                    if Message.objects.filter(language__title=language.title, title=self.title, number=self.number).count() == 0:

                        translated = Message()
                        translated.title = self.title
                        translated.text = self.text
                        translated.number = self.number
                        translated.language = language

                        translated.save(translate=False)

            else:

                super(Message, self).save(*args, **kwargs)

        else:

            super(Message, self).save(*args, **kwargs)

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

    active = models.BooleanField(
        "Active",
        default=False,
        blank=False,
        null=False
        )

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:

                for language in Language.objects.all():

                    if Button.objects.filter(language__title=language.title, button_code=self.button_code).count() == 0:

                        translated = Button()
                        translated.title = self.title
                        translated.button_code = self.button_code
                        translated.order = self.order
                        translated.active = self.active
                        translated.checkpoint = self.checkpoint
                        translated.language = language

                        translated.save(translate=False)

            else:

                super(Button, self).save(*args, **kwargs)

        else:

            super(Button, self).save(*args, **kwargs)

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

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:

                for language in Language.objects.all():

                    if Announcement.objects.filter(language__title=language.title, title=self.title).count() == 0:

                        translated = Announcement()
                        translated.language = language
                        translated.visible = self.visible
                        translated.active = self.active
                        translated.photo = self.photo
                        translated.title = self.title
                        translated.text = self.text

                        translated.save(translate=False)

            else:

                self.updated_at = timezone.now()
                super(Announcement, self).save(*args, **kwargs)

        else:

            self.updated_at = timezone.now()
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

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:

                for language in Language.objects.all():

                    if Event.objects.filter(language__title=language.title, title=self.title).count() == 0:

                        translated = Event()
                        translated.language = language
                        translated.visible = self.visible
                        translated.active = self.active
                        translated.photo = self.photo
                        translated.title = self.title
                        translated.text = self.text

                        translated.save(translate=False)

            else:

                self.updated_at = timezone.now()
                super(Event, self).save(*args, **kwargs)

        else:

            self.updated_at = timezone.now()
            super(Event, self).save(*args, **kwargs)


class Category(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )

    code = models.CharField(
        "Unique Code",
        default=1,
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
        on_delete=models.CASCADE,
        blank=True,
        null=True
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

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:
                self.code = str(hashlib.md5(self.title.encode('utf-8')).hexdigest())

                for language in Language.objects.all():

                    if Category.objects.filter(language__title=language.title, title=self.title, code=self.code).count() == 0:

                        translated = Category()
                        translated.language = language
                        translated.order = self.order
                        translated.photo = self.photo
                        translated.title = self.title
                        translated.description = self.description
                        translated.active = self.active
                        translated.code = self.code

                        translated.save(translate=False)

            else:

                super(Category, self).save(*args, **kwargs)

        else:

            super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.language.title} - {self.code} - {self.title}'


class Product(models.Model):

    title = models.CharField(
        "Title",
        default=None,
        max_length=255,
        blank=False,
        null=False
        )
    
    code = models.CharField(
        "Unique Code",
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

    def save(self, translate=True, *args, **kwargs):


        if translate:

            if self.pk is None:
                
                self.code = str(hashlib.md5(self.title.encode('utf-8')).hexdigest())

                for language in Language.objects.all():

                    if Product.objects.filter(language__title=language.title, title=self.title).count() == 0:

                        translated = Product()
                        translated.title = self.title
                        translated.code = self.code

                        filtered_cat = Category.objects.filter(code=self.category.code, language=language)

                        if filtered_cat.count() != 0:

                            translated.category = filtered_cat.first()

                        else:

                            translated_cat = Category()
                            translated_cat.language = language
                            translated_cat.order = self.category.order
                            translated_cat.photo = self.category.photo
                            translated_cat.title = self.category.title
                            translated_cat.description = self.category.description
                            translated_cat.active = self.category.active
                            translated_cat.code = self.category.code
                            translated_cat.save(translate=False)

                            translated.category = translated_cat

                        translated.description = self.description
                        translated.price = self.price
                        translated.photo = self.photo
                        translated.active = self.active
                        translated.order = self.order
                        translated.language = language

                        translated.save(translate=False)

            else:

                super(Product, self).save(*args, **kwargs)

        else:

            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.language.title} - {self.title}'


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

    def get_price(self):

        price_per_one = self.product.price
        price = price_per_one * self.count

        return price

    def __str__(self):
        return f'{self.product.title} - {self.count}'


class CartBase(models.Model):

    positions = models.ManyToManyField(Position)

    active = models.BooleanField(
        'Active',
        default=True,
        null=False,
        blank=False
        )
    
    canceled = models.BooleanField(
        'Canceled',
        default=False,
        null=False,
        blank=False
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

    def get_price(self):

        total = 0

        for position in self.positions.all():
            total += position.get_price()
        return total

    def get_count(self):

        count = 0

        for position in self.positions.all():
            count += position.count
        return count

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(CartBase, self).save(*args, **kwargs)


class OrderStatus(models.Model):

    title = models.CharField(
        'Title',
        max_length=256,
        null=False,
        blank=False
        )

    order = models.IntegerField(
        'Status Number',
        default=0,
        blank=False,
        null=False
        )

    def __str__(self):
        return f'{self.title} - {self.order}'

class OrderBase(models.Model):

    delivery = models.BooleanField(
        'Delivery',
        default=False,
        null=False,
        blank=False
        )

    time = models.CharField(
        "Time",
        default='Ближайшее время',
        max_length=1024,
        blank=False,
        null=False
        )

    card = models.BooleanField(
        'Card',
        default=False,
        null=False,
        blank=False
        )

    phone = models.BigIntegerField(
        'Phone',
        default=0,
        blank=False,
        null=False
        )

    name = models.CharField(
        "Name",
        default='',
        max_length=1024,
        blank=False,
        null=False
        )

    active = models.BooleanField(
        'Active',
        default=True,
        null=False,
        blank=False
        )

    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.CASCADE
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

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(OrderBase, self).save(*args, **kwargs)


class Region(models.Model):

    title = models.CharField(
        'Title',
        max_length=10,
        null=False,
        blank=False
        )

    def __str__(self):
        return self.title


class BranchTitle(models.Model):

    title = models.CharField(
        'Title',
        max_length=255,
        null=False,
        blank=False
        )

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="branch_language",
        blank=True,
        null=True,
        )

    def save(self, translate=True, *args, **kwargs):

        if translate:

            if self.pk is None:

                for language in Language.objects.all():

                    if BranchTitle.objects.filter(language__title=language.title, title=self.title).count() == 0:

                        translated = Message()
                        translated.title = self.title
                        translated.language = language

                        translated.save(translate=False)

            else:

                super(BranchTitle, self).save(*args, **kwargs)

        else:

            super(BranchTitle, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BranchBase(models.Model):

    title = models.ManyToManyField(
        BranchTitle
    )

    code = models.CharField(
        "Unique Code",
        default='',
        max_length=255,
        blank=False,
        null=False
        )

    description = models.CharField(
        'Description',
        max_length=255,
        default=""
        )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE
    )
    
    active = models.BooleanField(
        'Active',
        default=True,
        null=False,
        blank=False
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
    
    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(BranchBase, self).save(*args, **kwargs)

    # def __str__(self):
    #     return 