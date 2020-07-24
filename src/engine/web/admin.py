from django.contrib import admin
import web.models as models
from mptt.admin import MPTTModelAdmin

# Register your models here.
admin.site.register(models.Message, MPTTModelAdmin)
admin.site.register(models.Button, MPTTModelAdmin)
