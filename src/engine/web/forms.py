from django.forms import ModelForm
import core.models as core_models


class CategoryForm(ModelForm):
    class Meta:
        model = core_models.Category
        fields = ['title', 'description', 'active', 'order', 'photo']