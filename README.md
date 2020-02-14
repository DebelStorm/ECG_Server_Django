# ECG_Server_Django

## Python Pip Packages

```
Package             Version   
------------------- ----------
asgiref             3.2.3     
base32-lib          1.0.1     
certifi             2019.11.28
chardet             3.0.4     
defusedxml          0.6.0     
Django              3.0.2     
django-allauth      0.41.0    
django-otp          0.8.1     
django-rest-auth    0.9.5     
djangorestframework 3.11.0    
httpie              2.0.0     
idna                2.8       
mysqlclient         1.4.6     
oauthlib            3.1.0     
pip                 20.0.2    
Pygments            2.5.2     
pyotp               2.3.0     
python3-openid      3.1.0     
pytz                2019.3    
requests            2.22.0    
requests-oauthlib   1.3.0     
setuptools          45.0.0    
six                 1.14.0    
sqlparse            0.3.0     
urllib3             1.25.7    
wheel               0.33.6  
```
## APIs

* [Create User](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#create-user) : http://127.0.0.1/api/create_user
* [Update User](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#update-user) : http://127.0.0.1/api/update_user
* [Forgot Password](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#forgot-password) : http://127.0.0.1/api/forgot_password
* [Add Device](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#add-device) : http://127.0.0.1/api/add_device
* [Delete Device](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#delete-device) : http://127.0.0.1/api/delete_device
* [Update Device Settings](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#update-device-settings) : http://127.0.0.1/api/update_device_settings
* [Add Patient](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#add-patient) : http://127.0.0.1/api/add_patient
* [Post File](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#post-data) : http://127.0.0.1/api/post_data
* [Download File](https://github.com/DebelStorm/ECG_Server_Django/new/master?readme=1#get-data) : http://127.0.0.1/api/get_data

## API Request Format

Login and Logout API is required only when using browser. **For the rest of the APIs, pass Authentications details (Username and Password) with the request if required.**

Authentication used in postman : BasicAuth

### Create User

POST Request.

Local host link : http://127.0.0.1/api/create_user

Currently reserved only for superusers

Json Format
```
{
    "username": "",
    "password": "",
    "Confirm_Password": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "phone_number": ""
}
```

### Update User

PATCH Request.

Local host link : http://127.0.0.1/api/update_user

User Authentication Required.

Json Format
```
{
    "username": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "phone_number": ""
}
```


### Forgot Password

This Request has two modes. 
* Mode 1 - Request OTP
* Mode 2 - Change Password using OTP

#### Mode 1 : Requesting OTP

POST Request.

Local host link : http://127.0.0.1/api/forgot_password

No User Authentication Required.

Json Format
```
{
    "username": "",
    "email": ""
}
```

If username and email are correct, an OTP will be generated and send to the registered email.

#### Mode 2 : Changing Password using OTP

POST Request.

Local host link : http://127.0.0.1/api/forgot_password

No User Authentication Required.

Json Format
```
{
    "username": "",
    "email": "",
    "OTP": "",
    "new_password": "",
    "new_password_confirm": ""
}
```
### Add Device

POST Request.

Local host link : http://127.0.0.1/api/add_device

User Authentication Required. 

Json Format
```
{
    "device_name": "",
    "serial_number": "",
    "Mac_id": "",
    "Num_of_Leads": ""
}
```
Creates a new device object and a map to user_device_map table. If device is already present, only the map will be created. 

### Delete Device

POST Request.

Local host link : http://127.0.0.1/api/delete_device

User Authentication Required. 

Json Format
```
{
    "serial_number": ""
}
```
Only the users who have map in user_device_map for the device or, a superuser can delete device.

### Update Device Settings

POST Request.

Local host link : http://127.0.0.1/api/update_device_settings

User Authentication Required. 

Json Format
```
{
    "serial_number" : "",
    "device_name" : "",
    "Firmware_version_id" : "",
    "Firmware_version_number" : "",
    "Mac_id" : "",
    "Num_of_Leads" : ""
}
```
"serial_number" identifies the device. Only the users who have map in user_device_map for the device or, a superuser can update the device.

### Add Patient

POST Request.

Local host link : http://127.0.0.1/api/add_patient

User Authentication Required. 

Json Format

```
{
    "patient_name" : "",
    "patient_number" : ""
}
```

### Post Data

POST Request.

Local host link : http://127.0.0.1/api/post_data

User Authentication Required. 

Form Format

Content-Type : multipart/form-data
```
data_id - ""
device_sl_no - ""
patient_no - ""
File - (File to upload)
Start_Time - "HH:MM:SS.SSSS"
End_Time - "HH:MM:SS.SSSS"
```

"data_id" wil uniquely identify a file.

Must be uploaded via FORM Data.

### Get Data

GET Request.

Local host link : http://127.0.0.1/api/get_data

User Authentication Required. 

```
{
    "data_id" : ""
}
```

"data_id" wil uniquely identify a file.

Downloads the file with id "data_id".



