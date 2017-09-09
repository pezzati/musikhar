**EditProfile**
----
    user edit_profile

* **URL**

      /user/profile

* **Method:**

   `POST``GET`

* **Data Params**

        {
            "username": <username>,
            "birth_date": <birth_date>
            "image": <image>,
            "mobile": <mobile>
            "email": <email>,
            "bio": <bio>
            "first_name": <first_name>,
            "last_name": <last_name>
            "gender":<gender>,
        }

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{data: <data>}`

* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:**

        [
            {
                "error": "نام کاربری یا رمز کاربری وارد شده معتبر نمی باشد"
            },
            {
                "error": "نام کاربری یا رمز کاربری وارد شده معتبر نمی باشد"
            }
        ]

* **Sample Call:**

      curl -X POST -H "Content-Type: application/json" -d '{"username":"test_user",
            "password":"123456",
            "birth_date": <birth_date>,
            "image": <image>,
            "mobile": <mobile>
            "email": <email>,
            "bio": <bio>
            "first_name": <first_name>,
            "last_name": <last_name>
            "gender":<gender>, }' http://127.0.0.1:8000/user/profile
* **Notes:**

POST :Users can update their profile data in this view
GET  :Users can get their profile data in this view






    * **** 9 September by Soroush
