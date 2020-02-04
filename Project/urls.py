
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
# router = routers.DefaultRouter()

# router.register('users', UserViewSet)

urlpatterns = [
    #path('', UserListView.as_view()),
    path('', admin.site.urls),
    path('users/',include('user_api.urls')),
    path('devices/',include('device.urls')),
    path('patients/',include('patient.urls')),
    path('file/',include('data.urls')),
    #path('users/devices/',include('misc.urls')),
]


urlpatterns += [
    path('api/', include('rest_framework.urls')),
]
