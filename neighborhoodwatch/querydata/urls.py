from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tableSelection", views.tableSelection, name="tableSelection")
]