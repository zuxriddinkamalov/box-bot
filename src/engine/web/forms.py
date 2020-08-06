from django.forms import ModelForm
import core.models as core_models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from django.forms import inlineformset_factory


class CategoryForm(ModelForm):
    title = forms.CharField(max_length=255, required=True, label='Название')
    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
    )
    active = forms.BooleanField(label='Активность')
    
    order = forms.CharField(label='Порядковый номер')
    # photo = forms.FileField()
    
    class Meta:
        model = core_models.Category
        fields = ['title', 'description', 'active', 'order', 'photo']
        

PhotoFormSet = inlineformset_factory(core_models.Photo, core_models.Category,
                                            form=CategoryForm, extra=1)
