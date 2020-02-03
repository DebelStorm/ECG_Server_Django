from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserListView, UserCreateView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view()),  
    path('list/', UserListView.as_view()),
    path('add_user/', UserCreateView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
