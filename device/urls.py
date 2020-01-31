from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ShowAllDevices, AddDeleteDevice, add_device

urlpatterns = [
    path('', ShowAllDevices.as_view()),
    path('<int:pk>/', AddDeleteDevice.as_view()),
    path('add_device/', add_device),
]

urlpatterns = format_suffix_patterns(urlpatterns)
