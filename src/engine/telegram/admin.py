from django.contrib import admin
import telegram.models as models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Cart)
admin.site.register(models.PaySystem)
admin.site.register(models.Settings)

