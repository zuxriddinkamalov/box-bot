from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import core.models as core_models

# Create your models here.
class Message(MPTTModel):

    is_start = models.BooleanField(default=False)
    
    language = models.ForeignKey(
        core_models.Language,
        on_delete=models.CASCADE,
        related_name='web_message_language'
        )

    message = models.ForeignKey(core_models.Message, on_delete=models.CASCADE)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="prevMessage", blank=True, null=True)

    # class MPTTMeta:
    #     order_insertion_by = ['next']

    def __str__(self):
        return f"{self.message.title}"
    
    
class Button(MPTTModel):

    button = models.ForeignKey(core_models.Button, on_delete=models.CASCADE)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="prevButton", blank=True, null=True)

    # class MPTTMeta:
    #     order_insertion_by = ['next']

    def __str__(self):
        return f"{self.button.title}"
