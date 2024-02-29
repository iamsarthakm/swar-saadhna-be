from craft_audios import views
from django.urls import path

urlpatterns = [
    path("", views.Create.as_view()),
]
