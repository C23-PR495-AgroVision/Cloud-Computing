# Cloud-Computing

## Berbagai endpoint yang digunakan terdiri atas berbagai berikut

| OPERATION     | ENDPOINT      	    |
| ------------- | ------------------------- |
| POST          | /userHandler  	    |
| POST          |  /signin      	    |
| POST          |  /signout     	    |
| POST          |  /userHistory 	    |
| POST          |/reset-password	    |
| PUT		|/user/:uid/name	    |
| GET		|/user/:uid		    |
| POST		|/user/:uid/profile-picture |




## POST /userHandler

bertugas untuk mendaftarkan user kepada aplikasi

Request Body sebagai berikut:

```json
{
    "emailField": "kfgjdfkjs@gmail.com",
    "fullnameField": "nametest",
    "passwordField": "passwordtest123"
}
```

response yang sukses:

```json
{
    "status": "success",
    "message": "Sign-up has been successful",
    "data": {
        "user_id": "kejgT4WlafYbjhcI5kn2xUPb8gh1"
    }
}
```

Jika ada salah satu dari tiga field (emailField, fullnameField, passwordField) kosong:
```json

{
      "status": "fail",
      message: "All fields need to be filled. (Email, Full name, and Password)",
}
```

Jika terdapat error dalam membuat dokumen ke database, atau membuat akun user:
```json
{
        "status": "fail",
        "message": "An error occurred during sign-up",
}
```


## POST /signin

bertugas untuk me-login user kepada aplikasi

Request body sebagai berikut:

```json
{
    "email": "kfgjdfkjs@gmail.com",
    "password": "passwordtest123"
}
```

response yang sukses:
```json
{
    "status": "success",
    "message": "Sign-in successful",
    "user": {
        "uid": "kejgT4WlafYbjhcI5kn2xUPb8gh1",
        "email": "kfgjdfkjs@gmail.com"
    }
}
```

Jika salah satu field (email, password) tidak terisi:
```json
{
      "status": "fail",
      "message": "Email and password are required.",
}
```

Jika terdapat error dalam melakukan proses sign-in:
```json
{
        "status": "fail",
        "message": "An error occurred during sign-in",
}
```



## POST /signout

bertugas untuk me-logout user dari aplikasi.

Tidak perlu request body.

Response yang sukses:

```json
{
    "status": "success",
    "message": "Sign-out successful"
}
```

Jika terdapat error dalam melakukan proses sign-out:
```json
{
        "status": "fail",
        "message": "An error occurred during sign-out",
}
```

## POST /userHistory

bertugas untuk menyimpan hasil prediksi user dalam database.

Request body sebagai berikut:

```json
{
    "userId": "123456",
    "history": {
        "prediction1": "result1",
        "prediction2": "result2"
    }
}
```

Response yang sukses:
```json
{
       "message": "User history saved successfully"
}
```


## POST /reset-password

bertugas untuk mengirim email kepada user untuk melakukan proses reset password.

Request body sebagai berikut:

```json
{
    "email": "example@gmail.com"
}
```

response yang sukses:

```json
{
    "status": "success",
    "message": "Password reset email sent successfully."
}
```

Jika field yang diperlukan (email) kosong:
```json
{
      "status": "fail",
      "message": "Email is required."
}
```

Jika terdapat error saat melakukan proses pengiriman email password reset:

```json
{
        "status": "fail",
        "message": "An error occurred while sending the password reset email."
}
```

## PUT /user/:uid/name

Bertugas untuk menggantikan nama dari uid yang dibacakan.
Request parameter yang diperlukan adalah userid yang dimiliki user.

Request body sebagai berikut:

```json
{
    "uid": "kejgT4WlafYbjhcI5kn2xUPb8gh1",
    "name" : "namechangetest"
}
```

response yang sukses:

```json
{
    "status": "success",
    "message": "Name updated successfully."
}
```


Jika salah satu request (uid, name) kosong:
```json
{
      "status": "fail",
      "message": "UID and name are required."
}
```

Jika berdasarkan uid yang dimiliki, dokumen yang dicari tidak didapatkan:

```json
{
        "status": "fail",
        "message": "User not found."
}
```

Jika terdapat error sewaktu melakukan proses penggantian nama:
```json
{
      "status": "fail",
      "message": "An error occurred while updating name."
}
```

## GET /user/:uid

Bertugas untuk mengambil informasi user berdasarkan uid yang dibacakan.

Tidak perlu request body dalam bentuk JSON.
Hanya perlu request parameter dalam bentuk uid yang dimiliki user.

response yang sukses:

```json
{
    "status": "Success",
    "user": {
        "uid": "user_id_yang_terinput",
        "email": "example@gmail.com"
    }
}
```

Jika tidak menemukan dokumen yang bernama sama dengan uid user:

```json
{
        "status": "Failed",
        "message": "Data not found"
}
``` 

Jika terdapat error dalam proses mengambil informasi user:

```json
{
      "status": "Failed",
      "message": "Error retrieving user data"
}
```


## POST /user/:uid/profile-picture

Bertugas untuk memasukkan foto profile yang ingin digunakan. 
Request parameter adalah uid yang dimiliki oleh user.

Request body dalam bentuk file yang seperti screenshot berikut



Response yang sukses:

```json
{
      "status": "success",
      "message": "Profile picture added successfully."
}
```

Jika salah satu field (uid, profilePicture) kosong:

```json
{
      "status": "fail",
      "message": "UID and profile picture are required."
}
```

Jika tidak terdapat dokumen yang bernama uid tersebut:

```json
{
       "status": "fail",
        "message": "User not found."
}
```

Jika terdapat error sewaktu melakukan proses penambahan foto profile:

```json
{
     "status": "fail",
      "message": "An error occurred while adding profile picture."
}
```


