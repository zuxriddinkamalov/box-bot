from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from web.views import AllMessages, Dashboard, CategoryView, CategoryEditView, \
                        CategoryDeleteView, CategoryNewView, CategoryNewImageView

from web.views import ProductView, ProductEditView, ProductNewImageView, ProductNewView, ProductDeleteView
from web.views import newsView, newsEditView, newsNewImageView, newsNewView, newsDeleteView
from web.views import eventsView, eventsEditView, eventsNewImageView, eventsNewView, eventsDeleteView

from web.views import OrderList, OrderSingle

urlpatterns = [
    path('message/<str:language>/', AllMessages, name="all-messages"),
    path('', Dashboard, name="dashboard"),
    
    path('orders/', OrderList, name="orders"),
    path('orders/show/<int:pk>/', OrderSingle, name="order-single"),
    
    path('<str:language>/categories/', CategoryView, name="category"),
    path('<str:language>/categories/<int:pk>/edit/', CategoryEditView, name="category-edit"),
    path('categories/<int:pk>/new/', CategoryNewImageView, name="category-new-image"),
    path('categories/new/', CategoryNewView, name="category-new"),
    path('<str:language>/categories/<int:pk>/delete/', CategoryDeleteView, name="category-delete"),
    
    path('<str:language>/products/', ProductView, name="product"),
    path('<str:language>/products/<int:pk>/edit/', ProductEditView, name="product-edit"),
    path('products/<int:pk>/new/', ProductNewImageView, name="product-new-image"),
    path('products/new/', ProductNewView, name="product-new"),
    path('<str:language>/products/<int:pk>/delete/', ProductDeleteView, name="product-delete"),
    
    path('<str:language>/news/', newsView, name="news"),
    path('<str:language>/news/<int:pk>/edit/', newsEditView, name="news-edit"),
    path('news/<int:pk>/new/', newsNewImageView, name="news-new-image"),
    path('news/new/', newsNewView, name="news-new"),
    path('<str:language>/news/<int:pk>/delete/', newsDeleteView, name="news-delete"),
    
    path('<str:language>/events/', eventsView, name="events"),
    path('<str:language>/events/<int:pk>/edit/', eventsEditView, name="events-edit"),
    path('events/<int:pk>/new/', eventsNewImageView, name="events-new-image"),
    path('events/new/', eventsNewView, name="events-new"),
    path('<str:language>/events/<int:pk>/delete/', eventsDeleteView, name="events-delete"),

]


urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': "media/" + settings.MEDIA_ROOT, }),]