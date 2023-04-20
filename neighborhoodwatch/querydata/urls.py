from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("agencySelection", views.agencySelection, name="agencySelection"),
    path("parameterSelection", views.parameterSelection, name="parameterSelection")
]