from django.shortcuts import render
import web.models as web_models
import telegram.models as telegram_models
import core.models as core_models
from web.forms import CategoryForm

from django.http import HttpResponseRedirect, HttpResponse

from datetime import date, timedelta, time, datetime


def AllMessages(request, language):

    return render(request, "web/all_messages.html", {
        "messages": Message.objects.filter(language__title=language),
    })


def Dashboard(request):
    
    week = date.today()-timedelta(days=7)
    today = date.today()

    return render(request, "web/dashboard.html", {
        'total_users': telegram_models.User.objects.all().count(),
        'total_orders': telegram_models.Order.objects.filter(active=False).count(),
        "today_users": telegram_models.User.objects.filter(createdAt__day=today.day).count(),
        "today_orders": telegram_models.Order.objects.filter(created_at__day=today.day).count(),
        
    })
    
    
def CategoryEditView(request, language, pk):
    
    if request.method == 'POST':
        if not request.FILES:
            category = core_models.Category.objects.get(pk=pk)
            category.title = str(request.POST['title'])
            category.description = str(request.POST['description'])
            category.active = True if int(request.POST['active']) else False
            category.order = int(request.POST['order'])
            category.save()
            
            return HttpResponse('OK', status=200)
        else:
            category = core_models.Category.objects.get(pk=pk)
            
            uploaded_file = request.FILES['file']
            new_photo = core_models.Photo()
            new_photo.photo = uploaded_file
            new_photo.title = category.title
            
            new_photo.save()
            
            category = core_models.Category.objects.get(pk=pk)
            category.photo = new_photo
            category.save()
            
            return HttpResponse('Files', status=200)
    
    else:
    
        return render(request, "web/category_edit.html", {
            'category': core_models.Category.objects.get(id=pk)
        })
    
    
def CategoryView(request, language):
    
    return render(request, "web/category.html", {
        'all_categories': core_models.Category.objects.filter(language__title=language).order_by("order"),
    })


def StorylineEdit(request, slug):

    return render(request, "web/editStoryline.html", {
        "messages": Message.objects.filter(storyline__slug=slug),
        "storyline": Storyline.objects.get(slug=slug)
    })