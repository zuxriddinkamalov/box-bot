from django.shortcuts import render
import web.models as web_models
import telegram.models as telegram_models
import core.models as core_models
from web.forms import CategoryForm

from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator

from datetime import date, timedelta, time, datetime
import logging

logger = logging.getLogger(__name__)


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

class CategoryCreate(CreateView):
    model = core_models.Category
    fields = ['title', 'description', 'active', 'order', 'photo']
    
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        data = super(CategoryCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = FamilyMemberFormSet(self.request.POST)
        else:
            data['familymembers'] = FamilyMemberFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ProfileFamilyMemberCreate, self).form_valid(form)
    
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
            'category': core_models.Category.objects.get(id=pk),
            'products': core_models.Product.objects.filter(category__id=pk),
            'form': CategoryForm(instance=core_models.Category.objects.get(id=pk))
        })
    
    
def CategoryView(request, language):
    return render(request, "web/category.html", {
        'all_categories': core_models.Category.objects.filter(language__title=language).order_by("order"),
        '2nd_lan': core_models.Language.objects.exclude(title=language).first()
    })


def CategoryNewView(request):
    if request.method == 'POST':
        if not request.FILES:
            logger.error('not files')
            # logger.error(request.POST['title'])
            logger.error(request.FILES)
            logger.error(request.POST)
            
            
            
        else:
            logger.error('files')
            # logger.error(request.POST['title'])
            
            
        # category = core_models.Category()
        # category.title = str(request.POST['title'])
        # category.description = str(request.POST['description'])
        # category.active = True if int(request.POST['active']) else False
        # category.order = int(request.POST['order'])
        # category.save()
        # logger.error(category.save())
        # return HttpResponse(category.id, status=200)
        
    else:
        
        return render(request, "web/category_new.html", {
        })
        
def CategoryNewImageView(request, pk):
    if request.method == 'POST':
    
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

def CategoryDeleteView(request, language, pk):
    try:
        category = core_models.Category.objects.get(pk=pk)
        category.delete()
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        return HttpResponse(e, status=500)
    

def ProductEditView(request, language, pk):
    
    if request.method == 'POST':
        if not request.FILES:
            product = core_models.Product.objects.get(pk=pk)
            product.title = str(request.POST['title'])
            product.description = str(request.POST['description'])
            product.active = True if int(request.POST['active']) else False
            product.price = int(request.POST['price'])
            product.category = core_models.Category.objects.get(pk=int(request.POST['category']))
            product.order = int(request.POST['order'])
            product.save()
            
            return HttpResponse('OK', status=200)
        else:
            product = core_models.Product.objects.get(pk=pk)

            uploaded_file = request.FILES['file']
            new_photo = core_models.Photo()
            new_photo.photo = uploaded_file
            new_photo.title = product.title
            
            new_photo.save()
            
            product.photo = new_photo
            product.save()
            
            return HttpResponse('Files', status=200)
    
    else:
        
        return render(request, "web/product_edit.html", {
            'product': core_models.Product.objects.get(id=pk),
            'categories': core_models.Category.objects.filter(language__title=language)
        })
    
    
def ProductView(request, language):
    return render(request, "web/product.html", {
        'all_products': core_models.Product.objects.filter(language__title=language).order_by("order"),
        '2nd_lan': core_models.Language.objects.exclude(title=language).first()
    })


def ProductNewView(request):
    if request.method == 'POST':
        if not request.FILES:
            logger.error('not files')
            # logger.error(request.POST['title'])
            logger.error(request.FILES)
            logger.error(request.POST)
            
        else:
            logger.error('files')
            # logger.error(request.POST['title'])
            
            
        # category = core_models.Category()
        # category.title = str(request.POST['title'])
        # category.description = str(request.POST['description'])
        # category.active = True if int(request.POST['active']) else False
        # category.order = int(request.POST['order'])
        # category.save()
        # logger.error(category.save())
        # return HttpResponse(category.id, status=200)
        
    else:
        
        return render(request, "web/product_new.html", {
        })
        
def ProductNewImageView(request, pk):
    if request.method == 'POST':
    
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

def ProductDeleteView(request, language, pk):
    try:
        product = core_models.Product.objects.get(pk=pk)
        product.delete()
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        return HttpResponse(e, status=500)
    
def OrderList(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    
    orders = telegram_models.Order.objects.all().order_by('-created_at').order_by('active')
    p = Paginator(orders, 10)
    return render(request, "web/order_list.html", {
        'orders': p.page(page)
        })
    
def OrderSingle(request, pk):
    return render(request, "web/order_single.html", {
        'order': telegram_models.Order.objects.get(pk=pk)
        })
    
def newsEditView(request, language, pk):
    
    if request.method == 'POST':
        if not request.FILES:
            instance = core_models.Announcement.objects.get(pk=pk)
            instance.title = str(request.POST['title'])
            instance.text = str(request.POST['text'])
            instance.active = True if int(request.POST['active']) else False
            instance.visible = True if int(request.POST['visible']) else False
            instance.views = int(request.POST['views'])
            instance.save()
            
            return HttpResponse('OK', status=200)
        else:
            instance = core_models.Announcement.objects.get(pk=pk)

            uploaded_file = request.FILES['file']
            new_photo = core_models.Photo()
            new_photo.photo = uploaded_file
            new_photo.title = product.title
            
            new_photo.save()
            
            instance.photo = new_photo
            instance.save()
            
            return HttpResponse('Files', status=200)
    
    else:
        
        return render(request, "web/news_edit.html", {
            'instance': core_models.Announcement.objects.get(id=pk),
        })
    
    
def newsView(request, language):
    return render(request, "web/news.html", {
        'all': core_models.Announcement.objects.filter(language__title=language).order_by('-id'),
        '2nd_lan': core_models.Language.objects.exclude(title=language).first()
    })


def newsNewView(request):
    if request.method == 'POST':
        if not request.FILES:
            logger.error('not files')
            # logger.error(request.POST['title'])
            logger.error(request.FILES)
            logger.error(request.POST)
            
        else:
            logger.error('files')
            # logger.error(request.POST['title'])
            
            
        # category = core_models.Category()
        # category.title = str(request.POST['title'])
        # category.description = str(request.POST['description'])
        # category.active = True if int(request.POST['active']) else False
        # category.order = int(request.POST['order'])
        # category.save()
        # logger.error(category.save())
        # return HttpResponse(category.id, status=200)
        
    else:
        
        return render(request, "web/product_new.html", {
        })
        
def newsNewImageView(request, pk):
    if request.method == 'POST':
    
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

def newsDeleteView(request, language, pk):
    try:
        instance = core_models.Announcement.objects.get(pk=pk)
        instance.delete()
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        return HttpResponse(e, status=500)

def eventsEditView(request, language, pk):
    
    if request.method == 'POST':
        if not request.FILES:
            instance = core_models.Event.objects.get(pk=pk)
            instance.title = str(request.POST['title'])
            instance.text = str(request.POST['text'])
            instance.active = True if int(request.POST['active']) else False
            instance.visible = True if int(request.POST['visible']) else False
            instance.views = int(request.POST['views'])
            instance.save()
            
            return HttpResponse('OK', status=200)
        else:
            instance = core_models.Event.objects.get(pk=pk)

            uploaded_file = request.FILES['file']
            new_photo = core_models.Photo()
            new_photo.photo = uploaded_file
            new_photo.title = product.title
            
            new_photo.save()
            
            instance.photo = new_photo
            instance.save()
            
            return HttpResponse('Files', status=200)
    
    else:
        
        return render(request, "web/events_edit.html", {
            'instance': core_models.Event.objects.get(id=pk),
        })
    
    
def eventsView(request, language):
    return render(request, "web/events.html", {
        'all': core_models.Event.objects.filter(language__title=language).order_by("-id"),
        '2nd_lan': core_models.Language.objects.exclude(title=language).first()
    })


def eventsNewView(request):
    if request.method == 'POST':
        if not request.FILES:
            logger.error('not files')
            # logger.error(request.POST['title'])
            logger.error(request.FILES)
            logger.error(request.POST)
            
        else:
            logger.error('files')
            # logger.error(request.POST['title'])
            
            
        # category = core_models.Category()
        # category.title = str(request.POST['title'])
        # category.description = str(request.POST['description'])
        # category.active = True if int(request.POST['active']) else False
        # category.order = int(request.POST['order'])
        # category.save()
        # logger.error(category.save())
        # return HttpResponse(category.id, status=200)
        
    else:
        
        return render(request, "web/events_new.html", {
        })
        
def eventsNewImageView(request, pk):
    if request.method == 'POST':
    
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

def eventsDeleteView(request, language, pk):
    try:
        product = core_models.Product.objects.get(pk=pk)
        product.delete()
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        return HttpResponse(e, status=500)

