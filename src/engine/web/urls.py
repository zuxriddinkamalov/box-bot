from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from web.views import AllMessages, Dashboard, CategoryView, CategoryEditView


urlpatterns = [
    path('message/<str:language>/', AllMessages, name="all-messages"),
    path('', Dashboard, name="dashboard"),
    path('<str:language>/categories/', CategoryView, name="category"),
    path('<str:language>/categories/<int:pk>/edit/', CategoryEditView, name="category-edit"),
    
    
    
    # path('storyline/edit/<str:slug>', StorylineEdit, name="StorylineAdd"),

]


urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': "media/" + settings.MEDIA_ROOT, }),]