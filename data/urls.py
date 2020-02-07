from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import post_data_forms,get_data

urlpatterns = [
    path('upload/', post_data_forms.as_view()),
    path('download/<str:fileid>', get_data.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
