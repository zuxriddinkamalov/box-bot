from core.models import Message, Button, Announcement, Event, Product, Category
from django.db.models.signals import post_save


def translate_message(sender, instance, **kwargs):
    pass


def translate_button(sender, instance, **kwargs):
    pass


def translate_announcement(sender, instance, **kwargs):
    pass


def translate_event(sender, instance, **kwargs):
    pass


def translate_product(sender, instance, **kwargs):
    pass


def translate_category(sender, instance, **kwargs):
    pass


post_save.connect(translate_message, sender=Message)
post_save.connect(translate_button, sender=Button)
post_save.connect(translate_announcement, sender=Announcement)
post_save.connect(translate_event, sender=Event)
post_save.connect(translate_event, sender=Product)
post_save.connect(translate_event, sender=Category)
