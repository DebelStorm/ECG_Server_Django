from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ShowAllDevices, AddDeleteDevice

urlpatterns = [
    path('', ShowAllDevices.as_view()),
    path('<int:pk>/', AddDeleteDevice.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
