from django.urls import path
from . import views

urlpatterns = [
    path("", views.Audios.as_view()),
    path("taal", views.Taal.as_view()),
]
