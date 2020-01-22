from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserListView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
