**User Profile**
----

 Get or change user profile -- except profile image

* **URL**

      /user/profile

* **Method:**

    * to change `POST` 
    * to get `GET`

* **Data Params**
    To update User profile
    
        {
            "username": "new-user-name",
            "birth_date": <birth_date>,
            "mobile": "09366626525",
            "email": "test@test.com",
            "bio": "this is my test bio",
            "first_name": "my first name",
            "last_name": "my last name",
            "gender":<0 int for male and 1 int male>
        }
    
    * post call could have any of above parameters, or none!

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
