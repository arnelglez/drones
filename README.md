# Drones

## Description

Drones is a REST API created by Arnel González Rodríguez. This API is a small project propose by Musala Soft. This API was created with python and django framework using libraries as django rest framework, Pillow and  APscheduler.

### Files uses

`drones/api/drone_scheduler/drone_scheduler.py` This file contain tasks scheduler 
`drones/api/apps.py`    This file contain function ready, begin task scheduler  
`drones/api/models.py`  This file contain every models
`drones/api/serializers.py` This file contain serializers uses in API
`drones/api/tests.py`       This file contain Test functions
`drones/api/urls.py`        This file contain api URL
`drones/api/utils.py`       This file contain Mixins class and others functions
`drones/api/validators.py`  This file contain fields validations
`drones/api/views.py`       This file contain all views  

`drones/users/serializers.py` This file contain serializers uses in API
`drones/users/tests.py`       This file contain Test functions
`drones/users/urls.py`        This file contain users URL
`drones/users/utils.py`       This file contain Mixins class and others functions
`drones/users/validators.py`  This file contain fields validations
`drones/users/views.py`       This file contain all views  

`drones/drones/settings.py` This file contain project configurations
`drones/drones/urls.py`     This file contain root URL
`drones/drones/decorators.py`  This file contain

###  Requirements

`python 3.9.4`
`APScheduler==3.9.1`
`Django==4.0.7`
`djangorestframework==3.13.1`
`djangorestframework-simplejwt==4.8.0`
`django-cors-headers==3.13.0`
`drf-extra-fields==3.4.0`
`Pillow==9.2.0`

### Data format

#### User

```json
{ 
    "password1": password,
    "password2": confirm password,
    "is_superuser":  boolean ( 1 "True" or 0 "False"),
    "username": username,
    "first_name": first name,
    "last_name": last name,
    "email": email,
    "is_staff":  boolean ( 1 "True" or 0 "False")  
}
```

#### Drone

```json
{
    "serial": number 100 characters, 
    "model": integer 0 - 3, 
    "weight": float 0 - 100, 
    "battery": float 0 - 100, 
    "state": integer 0 - 5, 
}
```

#### Medication

```json
{
    "name" : allowed only letters, numbers, ‘-‘, ‘_’, 
    "weight" : float number, 
    "code" : allowed only upper case letters, underscore and numbers, 
    "image" : image encode64
}
```

#### Transportation

```json
{
    "drone" : drone id (integer),
    "medications" : 
        [
            # list of medications
            { 
                "medication": medication id (integer), 
                "amount": integer 
            }
        ],
    "status" : boolean ( 1 "True" or 0 "False")                
}
```


#### JUnit tests

Once python installed we need install requeriments.
Run command

```bash
pip3 install -r requirements.txt
```

For test begin, run command

```bash
python3 manage.py test
```
If you want aply test for app, you can use. 

```bash
python3 manage.py test api
python3 manage.py test users
```


Every test are begined with rigth data. If you want to try any validation only have to change var data and pass bad datas.


```python
    def test_create_drone(self):
        '''
        Ensure we can create a new drone object.
        '''
        url = reverse('drones_list')
        data = {"serial" : "1234567895", "model" : "3", "weight" : "200", "battery" : "70", "state" : "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(), 5)
```

In this case if you want a try failed of field serial, change serial in var data, for example next input is one of begined fields  

```python
data = {"serial" : "1234567890", "model" : "3", "weight" : "200", "battery" : "70", "state" : "1"} 

```

This in any var data you try change de datas inputs and you has one error like this     

```bash
  File "/dit/to/folder/drones/api/tests.py", line 29, in test_create_drone
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
AssertionError: 400 != 201

----------------------------------------------------------------------
Ran 24 tests in 0.376s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

#### Local execution

For local execution we have migrate ours model and start django local server, run commands.

```bash
python3 manage.py migrate

```
```bash
python3 manage.py runserver

```
Once server is start we have urls for all services, all urls are explain here


#### URLs

## Login

### Request

`POST /login/`

```bash
    curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"username" : "user1", "password" : "Pass123++"}' \
    http://localhost:8000/login/
```
### Response

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMDg2ODg2LCJpYXQiOjE2NjAwODY1ODYsImp0aSI6Ijk0ZDdiZTM2ZTc0YTQzYmJhODY0Mzc5ZDM3MWVlMmMwIiwidXNlcl9pZCI6MX0.kO3-9P0AWcwamZ1XOgQggk_G4oCpNojU8XF67h4POjI", 
    "referesh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDE3Mjk4NiwiaWF0IjoxNjYwMDg2NTg2LCJqdGkiOiJiN2JlMjFiOGRhYjA0NWQ4OWNlNTAzMWRhNzE0ZTZmMiIsInVzZXJfaWQiOjF9.cUosxG32Ac6QemsU1k2RR4WNDbIxDW3Pm_R0SXhuayA", 
    "user": {
                "id": 2, 
                "username": "user1", 
                "email": "user1z@email.com", 
                "first_name": "User", 
                "last_name": "Last Name"
            }
}
```

## Register

### Request

`POST /register/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{ "username" : "usertest", "password1" : "Prueba123+", "password2": "Prueba123+", "is_superuser":  "False", "first_name" : "Test", "last_name" : "User", "email" : "usertest@email.com", "is_staff":  "True" }' \
    http://localhost:8000/register/
```
### Response

```json
{
    "id": 4, 
    "last_login": null, 
    "is_superuser": false, 
    "username": "usertest", 
    "first_name": "Test", 
    "last_name": "User", 
    "email": "usertest@email.com", 
    "is_staff": true, 
    "is_active": true, 
    "date_joined": "2022-08-09T23:39:41.486247Z", 
    "groups": [], 
    "user_permissions": []
}
```

## Logout

### Request

`POST /logout/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \
    --header "Content-Type: application/json" \
    --request POST \
    http://localhost:8000/logout/
```
### Response

```json
"Successfully closed session"
```

## Drones List

### Request

`GET /api/drones/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drones/
```
### Response

```json
HTTP/1.1 200 OK
Date: Mon, 08 Aug 2022 00:17:11 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: application/json
Vary: Accept, Accept-Language, Cookie
Allow: GET, POST, HEAD, OPTIONS
Content-Language: en
X-Frame-Options: DENY
Content-Length: 931
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
    {
        "id": 1, 
        "serial": "123456760", 
        "model": 0, 
        "weight": 175.27, 
        "battery": 50.0, 
        "state": 1
    },
    ...
]

```
## Drones create

### Request

`POST /api/drones/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"serial" : "1234567895", "model" : "3", "weight" : "200", "battery" : "70", "state" : "0"}' \
    http://localhost:8000/api/drones/
```
### Response

```json
{
    "id": 11, 
    "serial": "1234567895", 
    "model": 3, 
    "weight": 200.0, 
    "battery": 70.0, 
    "state": 0
}
```

## Drone Details

### Request

`GET /api/drones/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drones/1/
```

### Response

```json
HTTP/1.1 200 OK
Date: Mon, 08 Aug 2022 00:33:37 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: application/json
Vary: Accept, Accept-Language, Cookie
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Language: en
X-Frame-Options: DENY
Content-Length: 91
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
    "id": 1, 
    "serial": "123456760", 
    "model": 0, 
    "weight": 175.27, 
    "battery": 50.0, 
    "state": 1
}
```
## Drone edit

### Request

`PUT /api/drones/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request PUT \
    --data '{"serial" : "1234567895", "model" : "4", "weight" : "450", "battery" : "75", "state" : "0"}' \
    http://localhost:8000/api/drones/11/
```
### Response

```json
{
    "id": 11, 
    "serial": "1234567895", 
    "model": 3, 
    "weight": 450, 
    "battery": 75, 
    "state": 0
}
```
## Drone delete

### Request

`DELETE /api/drones/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request DELETE \
    http://localhost:8000/api/drones/11/
```
### Response

```json

```

## Drones Availables

### Request

`GET /api/drones_availables/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drones_availables/
```

### Response

```json
HTTP/1.1 200 OK
Date: Mon, 08 Aug 2022 00:17:11 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: application/json
Vary: Accept, Accept-Language, Cookie
Allow: GET, POST, HEAD, OPTIONS
Content-Language: en
X-Frame-Options: DENY
Content-Length: 468
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
    {
        "id": 4, 
        "serial": "123456763", 
        "model": 1, 
        "weight": 272.98, 
        "battery": 65.0, 
        "state": 0
    },
    ...
]

```

## Drone batery status

### Request

`GET /api/drone_battery/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drone_battery/5/
```

### Response


```json
{
    "id": 5, 
    "battery": 65.0
}
```

## Drone medication list

### Request

`GET /api/drone_medications/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drone_medications/3/
```

### Response


```json
[
    {
        "id": 7, 
        "transportation": 3, 
        "medication": 1, 
        "medication_name": "ibuprofen", 
        "amount": 7
    }, 
    {
        "id": 8, 
        "transportation": 3, 
        "medication": 2, 
        "medication_name": "Aspirin", 
        "amount": 4
    }, 
    {
        "id": 9, 
        "transportation": 3, 
        "medication": 3, 
        "medication_name": "Paracetamol", 
        "amount": 7
    }, 
    {
        "id": 10, 
        "transportation": 3, 
        "medication": 4, 
        "medication_name": "Calergin", 
        "amount": 4
    }, 
    {
        "id": 11, 
        "transportation": 3, 
        "medication": 5, 
        "medication_name": "Mebendazol", 
        "amount": 4
    }
]
```
## Drone state

### Request

`POST /api/drone_state/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request POST \
    http://localhost:8000/api/drone_state/2/
```

### Response

```json
{
    "id": 2, 
    "serial": "123456761", 
    "model": 0, 
    "weight": 198.36, 
    "battery": 60.0, 
    "state": 
}
```

## Drones batery logs

### Request

`GET /api/drones_battery_logs`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drones_battery_logs/
```

### Response

```json
[
    {
        "id": 1, 
        "drone": 1, 
        "created_at": "2022-08-08T01:09:34.539320Z", 
        "battery": 50.0
    }, 
    {
        "id": 2, 
        "drone": 2, 
        "created_at": "2022-08-08T01:09:34.653351Z", 
        "battery": 60.0
    },
...
]
```

## Drone batery logs

### Request

`GET /api/drones_battery_logs/4/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/drones_battery_logs/4/
```

### Response

```json
[
    {
        "id": 4, 
        "drone": 4, 
        "created_at": "2022-08-08T01:09:34.874769Z", 
        "battery": 65.0
    }, 
    {
        "id": 14, 
        "drone": 4, 
        "created_at": "2022-08-08T01:11:14.148676Z", 
        "battery": 
        60.0
    }
]
```

## Medications List

### Request

`GET /api/medications/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/medications/
```
### Response

```json
HTTP/1.1 200 OK
Date: Mon, 08 Aug 2022 01:20:07 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: application/json
Vary: Accept, Accept-Language, Cookie
Allow: GET, POST, HEAD, OPTIONS
Content-Language: en
X-Frame-Options: DENY
Content-Length: 736
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
    
    {
        "id": 1, 
        "name": "ibuprofen", 
        "code": "AFAHHZZZ_1525157", 
        "weight": 12.0, 
        "image": "/media/medication/fa296439-bb3c-4c38-bb89-31c76e0df4b6.jpg"
    }, 
    {
        "id": 2, 
        "name": "Aspirin", 
        "code": "AFAHHZZZ_1525162", 
        "weight": 7.0, 
        "image": "/media/medication/aa5cf863-1da9-4bf4-aef3-7bb9053da421.jpg"
    }
    ...
]
```
## Medications create

### Request

`POST /api/medications/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"name" : "medications4", "weight" : "10", "code" : "FF_55555_DD", "image" : "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"}' \
    http://localhost:8000/api/medications/
```
### Response

```json
{
    "id": 6, 
    "name": "medications4", 
    "code": "FF_55555_DD", 
    "weight": 10.0, 
    "image": "/media/medication/02f5fd4c-f59d-4ff0-8098-8d696e5c7d20.jpg"
}
```

## Medication Details

### Request

`GET /api/medications/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/medications/1/
```

### Response

```json
{
    "id": 1, 
    "name": "ibuprofen", 
    "code": "AFAHHZZZ_1525157", 
    "weight": 12.0, 
    "image": "/media/medication/fa296439-bb3c-4c38-bb89-31c76e0df4b6.jpg"
}
```
## Medication edit

### Request

`PUT /api/medications/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request PUT \
    --data '{"name" : "new_medication_name", "weight" : "12.5", "code" : "FF_5HH55_DD", "image" : "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"}' \
    http://localhost:8000/api/medications/6/
```
### Response

```json
{
    "id": 6, 
    "name": "new_medication_name", 
    "code": "FF_5HH55_DD", 
    "weight": 12.5, 
    "image": "/media/medication/179c8b38-c694-4d98-a705-fb7749724c8f.jpg"
}
```
## Medication delete

### Request

`DELETE /api/medications/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request DELETE \
    http://localhost:8000/api/medications/6/
```
### Response

```json

```

## Transportations List

### Request

`GET /api/transportations/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/transportations/
```
### Response

```json
HTTP/1.1 200 OK
Date: Mon, 08 Aug 2022 01:31:13 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: application/json
Vary: Accept, Accept-Language, Cookie
Allow: GET, POST, HEAD, OPTIONS
Content-Language: en
X-Frame-Options: DENY
Content-Length: 1603
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
    {
        "id": 1, 
        "drone": 1, 
        "status": true, 
        "medications": 
            [
                {
                    "id": 1, 
                    "medication": 2, 
                    "medication_name": "Aspirin", 
                    "amount": 3
                }, 
                {
                    "id": 2, 
                    "medication": 4, 
                    "medication_name": "Calergin", 
                    "amount": 3
                }, 
                {
                    "id": 3, 
                    "medication": 1, 
                    "medication_name": "ibuprofen", 
                    "amount": 3
                }
            ]
    }, 
    {
        "id": 2, 
        "drone": 2, 
        "status": true, 
        "medications": 
            [
                {
                    "id": 4, 
                    "medication": 5, 
                    "medication_name": "Mebendazol", 
                    "amount": 7
                }, 
                {
                    "id": 5, 
                    "medication": 4, 
                    "medication_name": "Calergin", 
                    "amount": 4
                }, 
                {
                    "id": 6, 
                    "medication": 2, 
                    "medication_name": "Aspirin", 
                    "amount": 3
                    }
            ]
    }
...
]


```
## Transportations create

### Request

`POST /api/transportations/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request POST \
    --data '{ "drone":5, "medications":[{ "medication":2, "amount":3 }, { "medication":1, "amount":2 }], "status":1}' \
    http://localhost:8000/api/transportations/
```
### Response

```json
{
    "id": 6, 
    "drone": 5, 
    "status": true, 
    "medications": 
        [
            {
                "id": 19, 
                "medication": 2, 
                "medication_name": "Aspirin", 
                "amount": 3
            }, 
            {
                "id": 20, 
                "medication": 1, 
                "medication_name": "ibuprofen", 
                "amount": 2
            }
        ]
}
```

## Transportation Details

### Request

`GET /api/transportations/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/transportations/5/
```

### Response

```json
{
    "id": 5, 
    "drone": 8, 
    "status": true, 
    "medications": 
        [
            {
                "id": 17, 
                "medication": 1, 
                "medication_name": "ibuprofen",
                "amount": 13
            }, 
            {
                "id": 18, 
                "medication": 5, 
                "medication_name": "Mebendazol", 
                "amount": 20
            }
        ]
}
```
## Transportation edit

### Request

`PUT /api/transportations/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request PUT \
    --data '{ "drone":5, "medications":[{ "medication":1, "amount":2 }, { "medication":1, "amount":3 }], "status":1}' \
    http://localhost:8000/api/transportations/6/
```
### Response

```json
{
    "id": 6, 
    "drone": 5, 
    "status": true, 
    "medications": 
        [
            {
                "id": 21, 
                "medication": 1, 
                "medication_name": "ibuprofen", 
                "amount": 2
            }, 
            {
                "id": 22, 
                "medication": 1, 
                "medication_name": "ibuprofen", 
                "amount": 3
            }
        ]
}
```
## Transportation delete

### Request

`DELETE /api/transportations/id/`

```bash
    curl --header "Authorization: Bearer <ACCESS_TOKEN>" \ 
    --header "Content-Type: application/json" \
    --request DELETE \
    http://localhost:8000/api/transportations/6/
```
### Response

```json

``` 
   