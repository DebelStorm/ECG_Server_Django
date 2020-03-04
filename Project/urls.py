
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from user_api.views import UserListView, UserCreateView, UserDetailView, ForgotPassword, test_redirect, UserLoginView, UserLogoutView#, CurrentUserView
from device.views import add_device, update_device_settings, delete_device, get_ota, show_devices
from data.views import post_data_forms, get_data, get_data_via_browser
from patient.views import CreatePatient, UpdatePatient, DeletePatient#, RetrieveUpdateDeletePatient
from rest_framework.authtoken.views import obtain_auth_token
# router = routers.DefaultRouter()

# router.register('users', UserViewSet)

urlpatterns = [
    #path('', UserListView.as_view()),
    path('api/login', UserLoginView.as_view()),
    path('api/logout', UserLogoutView.as_view()),
    path('admin/', admin.site.urls),
    path('', test_redirect),
    path('api/create_user', UserCreateView.as_view()),
    path('api/update_user', UserDetailView.as_view()),
    path('api/list_users', UserListView.as_view()),
    path('api/forgot_password', ForgotPassword.as_view()),

    path('api/get_token', obtain_auth_token),

    path('api/add_device', add_device),
    path('api/show_devices', show_devices.as_view()),
    path('api/delete_device', delete_device),
    path('api/update_device_settings', update_device_settings),

    path('api/get_data', get_data.as_view()),
    path('api/get_data/<str:data_id>', get_data_via_browser.as_view()),
    path('api/post_data', post_data_forms.as_view()),

    path('api/add_patient', CreatePatient.as_view()),
    path('api/update_patient', UpdatePatient.as_view()),
    path('api/delete_patient', DeletePatient.as_view()),
    path('api/get_ota', get_ota.as_view()),
    #path('users/',include('user_api.urls')),
    #path('devices/',include('device.urls')),
    #path('patients/',include('patient.urls')),
    #path('file/',include('data.urls')),
    #path('users/devices/',include('misc.urls')),
    #path('api/', include('rest_framework.urls')),
]
