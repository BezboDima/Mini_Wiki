from urllib import request
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search,  name ="search"),
    path("new", views.new, name="new"),
    path("rand", views.rand, name="rand"),
    path("<str:name>/edit", views.edit, name="edit"),
    path("<str:name>", views.entry, name="entry")
]
