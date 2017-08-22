**Login**
----
    user login

* **URL**

      /user/login

* **Method:**

   `POST`

* **Data Params**

        {
            "username": <username>,
            "password": <password>
        }

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{token: <token_key>}`

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

      curl -X POST -H "Content-Type: application/json" -d '{"username":"test_user","password":"123456"}' http://127.0.0.1:8000/user/login
* **Notes:**

    * **Optional_login_with_Email_mobile** 22 August by Soroush
