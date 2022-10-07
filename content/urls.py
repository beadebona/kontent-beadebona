from django.urls import path

from content.views import ContentView

urlpatterns = [
    path("content", ContentView.as_view()),
]
