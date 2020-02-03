from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreatePatient, ListPatients, RetrieveUpdateDeletePatient#, DeletePatient

urlpatterns = [
    path('', ListPatients.as_view()),
    path('modify_patient/<int:pk>/', RetrieveUpdateDeletePatient.as_view()),
    path('add_patient/', CreatePatient.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
