# ECG_Server_Django

## Python Pip Packages

```
Package             Version   
------------------- ----------

07 Feb :

asgiref             3.2.3        
certifi             2019.11.28
chardet             3.0.4     
defusedxml          0.6.0     
Django              3.0.2     
django-allauth      0.41.0       
django-rest-auth    0.9.5     
djangorestframework 3.11.0    
httpie              2.0.0     
idna                2.8       
mysqlclient         1.4.6     
oauthlib            3.1.0     
pip                 20.0.2    
Pygments            2.5.2     
python3-openid      3.1.0     
pytz                2019.3    
requests            2.22.0    
requests-oauthlib   1.3.0     
setuptools          45.0.0    
six                 1.14.0    
sqlparse            0.3.0     
urllib3             1.25.7    
wheel               0.33.6   

19 Feb:

base32-lib          1.0.1  
django-otp          0.8.1
pyotp               2.3.0

10 March :

django-cleanup      4.0.0  
numpy               1.18.1
scipy               1.4.1
```

The packages can be also installed using the following command

```
pip install asgiref certifi chardet defusedxml Django django-allauth django-rest-auth djangorestframework httpie idna mysqlclient oauthlib Pygments python3-openid pytz requests requests-oauthlib setuptools six sqlparse urllib3 wheel base32-lib django-otp pip pyotp django-cleanup scipy numpy
```


Please update the db each time by running the following commands in the project directory.

```
python manage.py makemigrations
python manage.py migrate
```

## APIs

* [Login User](#login-user) : http://127.0.0.1/api/login
* [Logout User](#logout-user) : http://127.0.0.1/api/logout
* [Create User](#create-user) : http://127.0.0.1/api/create_user
* [Update User](#update-user) : http://127.0.0.1/api/update_user
* [Forgot Password](#forgot-password) : http://127.0.0.1/api/forgot_password
* [Add Device](#add-device) : http://127.0.0.1/api/add_device
* [Delete Device](#delete-device) : http://127.0.0.1/api/delete_device
* [Show Devices](#show-devices) : http://127.0.0.1/api/show_devices
* [Get OTA of Device](#get-ota-device) : http://127.0.0.1/api/get_ota
* [Update Device Settings](#update-device-settings) : http://127.0.0.1/api/update_device_settings
* [Add Patient](#add-patient) : http://127.0.0.1/api/add_patient
* [Update Patient Details](#update-patient) : http://127.0.0.1/api/update_patient
* [Delete Patient](#delete-patient) : http://127.0.0.1/api/add_patient
* [Show Patients](#show-patients) : http://127.0.0.1/api/show_patients
* [Post File - Raw Bin File](#post-raw-data) : http://127.0.0.1/api/post_raw_data
* [Post File - Proccessed File](#post-roccessed-data) : http://127.0.0.1/api/post_proccessed_data
* [Download File](#get-data) : http://127.0.0.1/api/get_data

## API Request Format

### Login User

Post Request

Local host link : http://127.0.0.1/api/login

JSON Format:

```
{
    "username": "",
    "password": ""
}
```

Will Return session_id. Example,

```
"abcdefgh1234567890abcdefghijklmnopqrstuv"
```

### Logout User

Post Request

Local host link : http://127.0.0.1/api/logout

JSON Format:

```
{
    "session_id" : ""
}
```

### Create User

POST Request.

Local host link : http://127.0.0.1/api/create_user

No Authentication Required

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

POST Request.

Local host link : http://127.0.0.1/api/update_user

User Authentication Required.

Json Format
```
{
    "session_id" : ""
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
    "session_id" : ""
    "device_name": "",
    "serial_number": "",
    "Mac_id": "",
    "Num_of_Leads": ""
}
```
Creates a new device object and a map to user_device_map table. If device is already present, only the map will be created. "serial_number" uniquely identifies a device.

### Delete Device

POST Request.

Local host link : http://127.0.0.1/api/delete_device

User Authentication Required.

Json Format
```
{
    "session_id" : ""
    "serial_number": ""
}
```
Only the users who have map in user_device_map for the device or, a superuser can delete device.

### Show Devices

POST Request.

Local host link : http://127.0.0.1/api/show_devices

User Authentication Required.

Json Format
```
{
    "session_id" : ""
}
```

Returns a list of JSON objects of devices registered by the current user. Eg:
```
{
    "status": "SUCCESS",
    "data": [
        {
            "device_name": "DeviceOfBetty",
            "serial_number": "Betty",
            "Mac_id": "Betty",
            "Num_of_Leads": 10,
            "Firmware_Version_id": " N/A ",
            "Firmware_version_number": " N/A "
        },
        {
            "device_name": "DeviceOfBetty1",
            "serial_number": "Betty2",
            "Mac_id": "Betty",
            "Num_of_Leads": 10,
            "Firmware_Version_id": " N/A ",
            "Firmware_version_number": " N/A "
        },
        {
            "device_name": "DeviceOfBetty1",
            "serial_number": "Betty3",
            "Mac_id": "Betty",
            "Num_of_Leads": 10,
            "Firmware_Version_id": " N/A ",
            "Firmware_version_number": " N/A "
        }
    ]
}
```

### Get OTA Device

POST Request.

Local host link : http://127.0.0.1/api/get_ota

User Authentication Required.

Json Format
```
{
    "session_id" : ""
    "serial_number": ""
}
```

Return data of device with the give serial number in the following JSON format:

```
{
    "status": "SUCCESS",
    "data": [
        {
            "device_name": "DeviceOfBetty",
            "serial_number": "Betty",
            "Mac_id": "Betty",
            "Num_of_Leads": 10,
            "Firmware_Version_id": " N/A ",
            "Firmware_version_number": " N/A "
        }
    ]
}
```

### Update Device Settings

POST Request.

Local host link : http://127.0.0.1/api/update_device_settings

User Authentication Required.

Json Format
```
{
    "session_id" : ""
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
    "session_id" : "",
    "serial_number" : "",
    "patient_name" : "",
    "patient_number" : ""
}
```

A new patient is mapped against the current user and a device with the given serial number. The device must be registered to the current user.

Patient number is unique and identifies the patient.

### Update Patient

POST Request.

Local host link : http://127.0.0.1/api/update_patient

User Authentication Required.

Json Format

```
{
    "session_id" : ""
    "patient_name" : "",
    "patient_number" : ""
}
```

Patient number identifies the patient. Will replace old patient Name with new patient name.

### Show Patients

POST Request.

Local host link : http://127.0.0.1/api/show_patients

User Authentication Required.

Json Format
```
{
    "session_id" : "",
    "serial_number" : ""
}
```

Returns a list of JSON objects of patients registered by the current user for an existing device. Eg:
```
{
    "status": "SUCCESS",
    "data": [
        {
            "patient_number": "1",
            "patient_name": "Adam"
        },
        {
            "patient_number": "2",
            "patient_name": "Bobby"
        }
    ]
}
```

### Delete Patient

POST Request

Local host link : http://127.0.0.1/api/delete_patient

User Authentication Required.

Json Format


```
{
    "session_id" : ""
    "patient_number" : ""
}
```


### Post Raw Data

POST Request.

Local host link : http://127.0.0.1/api/post_raw_data

User Authentication Required.

JSON Format

```
{
  "session_id" : "",
  "data_id" : "",         -> (Unique)
  "device_sl_no" : "",
  "patient_no" : "",
  "File_location" : "",   -> (Absolute file path)
  "Start_Time" : "",      -> (Epoch time)
  "End_Time" : "",        -> (Epoch time)
  "overwrite" : ""        -> (Optional, Default False)
}
```

"data_id" wil uniquely identify a file. To save the file location of raw bin files.

### Post Proccessed Data

POST Request.

Local host link : http://127.0.0.1/api/post_proccessed_data

User Authentication Required.

JSON Format

```
{
  "session_id" : "",
  "data_id" : "",         -> (Unique)
  "device_sl_no" : "",
  "patient_no" : "",
  "File_location" : "",   -> (Absolute file path)
  "Start_Time" : "",      -> (Epoch time)
  "End_Time" : "",        -> (Epoch time)
  "overwrite" : ""        -> (Optional, Default False)
}
```

"data_id" wil uniquely identify a file. To save file locations of proccessed files.


### Get Data

POST Request.

To get processed data of a patient recorded from a particular device, between a particular time period.

Local host link : http://127.0.0.1/api/get_data

User Authentication Required.

```
{
	"session_id" : "",
	"serial_number" : "",
	"patient_no" : "",
	"Start_Time" : "",
	"End_Time" : ""
}
```

Response will contain filtered data from all files between "Start_Time" and "End_Time" for the patient from the given device.

Format of response :
```
{
	"status" : "",
	"no_of_files" : "",
	"Start_Time_set" : [],
	"End_Time_set" : [],
	"No_of_records" : [],
	"Data" : [ [] , [] , ... , [] ]
}

```

Here, each element in "Data" contains data from each file in string format. for eg,

```
{
  "status" : "SUCCESS",
  "no_of_files" : "n",
  "Start_Time_set" : [0, 10, 20, .. ],
  "End_Time_set" : [10, 20, 30, .. ],
  "No_of_records" : [4, 4, ..., 4],
  "Data" :  [
              ["1.0,2.0,3.0" , "0.0,1.0,2.0" , "0.0,1.0,2.0" , "0.0,1.0,2.0"] ,   -> (file 1, 4 records)
              ["1.1,2.4,5.3" , "1.1,2.4,5.3" , "1.1,2.4,5.3" , "1.1,2.4,5.3"] ,   -> (file 2, 4 records)
              ... ,
              ["1.1,2.4,5.3" , "1.1,2.4,5.3" , "1.1,2.4,5.3" , "1.1,2.4,5.3"] ,   -> (file n, 4 records)
            ]
}
```
Please note that each string will contain comma seperated values up to the number of ECG signals that the file contains.
