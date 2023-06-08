# Cloud-Computing

##Berbagai endpoint yang digunakan terdiri atas berbagai berikut

| OPERATION     | ENDPOINT      |
| ------------- | ------------- |
| POST          | /userHandler  |
| POST          |  /signin      |
| POST          |  /signout     |


##POST /userHandler

bertugas untuk mendaftarkan user kepada aplikasi

Request Body sebagai berikut:

```json
{
    "emailField": "hmmmmmmhaha@gmail.com",
    "fullnameField": "falih budiman baruna",
    "passwordField": "passwordtest123"
}
```

response yang sukses:

```json
{
    "status": "success",
    "message": "Sign-up has been successful"
}
```


##POST /signin

bertugas untuk me-login user kepada aplikasi

Request body sebagai berikut:

```json
{
    "email": "hmmmmmmhaha@gmail.com",
    "password": "passwordtest123"
}
```

response yang sukses:
```json
{
    "status": "success",
    "message": "Sign-in successful",
    "user": {
        "email": "hmmmmmmhaha@gmail.com"
    }
}
```

##POST /signout

bertugas untuk me-logout user dari aplikasi.

Tidak perlu request body.

{
    "status": "success",
    "message": "Sign-out successful"
}
