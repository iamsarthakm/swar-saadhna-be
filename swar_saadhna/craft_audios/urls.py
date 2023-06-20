from craft_audios import views
from django.urls import path

urlpatterns = [
    path("create", views.Create.as_view()),
]