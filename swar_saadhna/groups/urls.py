from django.urls import path
from . import views

urlpatterns = [
    path("", views.Group.as_view()),
    path("audios", views.GroupAudios.as_view()),
    path("users", views.GroupUsers.as_view()),
    path("code", views.JoinGroup.as_view()),
]
