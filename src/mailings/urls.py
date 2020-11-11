from django.urls import path, include

from . import views

urlpatterns = [
    path('add_to_common_list', views.add_to_common_list_view),
]