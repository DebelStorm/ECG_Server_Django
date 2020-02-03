from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ShowAllDevices, DetailDevice, add_device, delete_device, update_device_settings

urlpatterns = [
    path('', ShowAllDevices.as_view()),
    path('<int:pk>/', DetailDevice.as_view()),
    path('add_device/', add_device),
    path('delete_device/', delete_device),
    path('update_device/', update_device_settings),
]

urlpatterns = format_suffix_patterns(urlpatterns)
