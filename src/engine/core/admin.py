from django.contrib import admin
import core.models as models

# Register your models here.
admin.site.register(models.Language)
admin.site.register(models.Message)
admin.site.register(models.Photo)
admin.site.register(models.Position)
admin.site.register(models.Product)
admin.site.register(models.Announcement)
admin.site.register(models.Event)
admin.site.register(models.CartBase)
admin.site.register(models.Category)
admin.site.register(models.OrderStatus)



@admin.register(models.Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'order',
                    'title',
                    'button_code',
                    'GetLanguage',
                    'checkpoint')

    def GetLanguage(self, obj):
        return obj.language.title
    GetLanguage.admin_order_field = 'language'
    GetLanguage.short_description = 'Language'

    ordering = ('id',
                'order',
                'checkpoint')
    search_fields = ('id', 'order')
