from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import post_data_forms

urlpatterns = [
    path('upload/', post_data_forms.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
