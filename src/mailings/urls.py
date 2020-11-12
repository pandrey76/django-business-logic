from django.urls import path, include

from . import views

urlpatterns = [
    path('add_to_common_list', views.add_to_common_list_view),
    path('add_to_case_list_view', views.add_to_case_list_view),
]
