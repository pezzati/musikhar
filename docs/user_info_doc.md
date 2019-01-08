**User Info**
----

 Get or change user profile info like name and birth date -- except profile image

* **URL**

      /user/profile

* **Method:**

    * to change `POST` 
    * to get `GET`

* **Data Params**
    To update User profile
    
        {
            "username": "new-user-name",
            "mobile": "09366626525",
            "email": "test@test.com",
            "first_name": "my first name",
            "last_name": "my last name",
            "avatar": 12
        }
    
    * post call could have any of above parameters, or none!

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    
        {
            "username": "peymanezzati",
            "mobile": "09366626525",
            "email": "peyman@test.ir",
            "first_name": "peyman",
            "last_name": "ezzati",
            "premium_days": 0,
            "coins" : 123,
            "avatar": {
                "link": "http://127.0.0.1:8000/uploads/default_avatars/bored-student.jpg",
                "id": 1
            }
        }

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
