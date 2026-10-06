from django.urls import path
from.import views
urlpatterns=[
    path("",views.index,name="index"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
] 
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("rejestracja/", views.rejestracja, name="rejestracja"),
    path("historia/", views.historia, name="historia"),
]